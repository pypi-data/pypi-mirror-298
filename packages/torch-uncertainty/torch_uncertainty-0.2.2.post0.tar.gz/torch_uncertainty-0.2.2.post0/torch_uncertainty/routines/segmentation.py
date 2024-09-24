import torch
from einops import rearrange
from lightning.pytorch import LightningModule
from lightning.pytorch.loggers import Logger
from lightning.pytorch.utilities.types import STEP_OUTPUT
from torch import Tensor, nn
from torch.optim import Optimizer
from torchmetrics import Accuracy, MetricCollection
from torchvision.transforms.v2 import functional as F

from torch_uncertainty.metrics import (
    AUGRC,
    AURC,
    BrierScore,
    CalibrationError,
    CategoricalNLL,
    MeanIntersectionOverUnion,
)
from torch_uncertainty.models import (
    EPOCH_UPDATE_MODEL,
    STEP_UPDATE_MODEL,
)


class SegmentationRoutine(LightningModule):
    def __init__(
        self,
        model: nn.Module,
        num_classes: int,
        loss: nn.Module,
        optim_recipe: dict | Optimizer | None = None,
        format_batch_fn: nn.Module | None = None,
        metric_subsampling_rate: float = 1e-2,
        log_plots: bool = False,
        num_calibration_bins: int = 15,
    ) -> None:
        r"""Routine for training & testing on **segmentation** tasks.

        Args:
            model (torch.nn.Module): Model to train.
            num_classes (int): Number of classes in the segmentation task.
            loss (torch.nn.Module): Loss function to optimize the :attr:`model`.
            optim_recipe (dict or Optimizer, optional): The optimizer and
                optionally the scheduler to use. Defaults to ``None``.
            format_batch_fn (torch.nn.Module, optional): The function to format the
                batch. Defaults to ``None``.
            metric_subsampling_rate (float, optional): The rate of subsampling for the
                memory consuming metrics. Defaults to ``1e-2``.
            log_plots (bool, optional): Indicates whether to log plots from
                metrics. Defaults to ``False``.
            num_calibration_bins (int, optional): Number of bins to compute calibration
                metrics. Defaults to ``15``.

        Warning:
            You must define :attr:`optim_recipe` if you do not use the CLI.

        Note:
            :attr:`optim_recipe` can be anything that can be returned by
            :meth:`LightningModule.configure_optimizers()`. Find more details
            `here <https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#configure-optimizers>`_.
        """
        super().__init__()
        _segmentation_routine_checks(
            num_classes,
            metric_subsampling_rate,
            num_calibration_bins,
        )

        self.model = model
        self.num_classes = num_classes
        self.loss = loss
        self.needs_epoch_update = isinstance(model, EPOCH_UPDATE_MODEL)
        self.needs_step_update = isinstance(model, STEP_UPDATE_MODEL)

        if format_batch_fn is None:
            format_batch_fn = nn.Identity()

        self.optim_recipe = optim_recipe
        self.format_batch_fn = format_batch_fn
        self.metric_subsampling_rate = metric_subsampling_rate
        self.log_plots = log_plots

        # metrics
        seg_metrics = MetricCollection(
            {
                "seg/mIoU": MeanIntersectionOverUnion(num_classes=num_classes),
            },
            compute_groups=False,
        )
        sbsmpl_seg_metrics = MetricCollection(
            {
                "seg/mAcc": Accuracy(
                    task="multiclass", average="macro", num_classes=num_classes
                ),
                "seg/Brier": BrierScore(num_classes=num_classes),
                "seg/NLL": CategoricalNLL(),
                "seg/pixAcc": Accuracy(
                    task="multiclass", num_classes=num_classes
                ),
                "cal/ECE": CalibrationError(
                    task="multiclass",
                    num_classes=num_classes,
                    num_bins=num_calibration_bins,
                ),
                "cal/aECE": CalibrationError(
                    task="multiclass",
                    adaptive=True,
                    num_bins=num_calibration_bins,
                    num_classes=num_classes,
                ),
                "sc/AURC": AURC(),
                "sc/AUGRC": AUGRC(),
            },
            compute_groups=[
                ["seg/mAcc"],
                ["seg/Brier"],
                ["seg/NLL"],
                ["seg/pixAcc"],
                ["cal/ECE", "cal/aECE"],
                ["sc/AURC", "sc/AUGRC"],
            ],
        )

        self.val_seg_metrics = seg_metrics.clone(prefix="val/")
        self.val_sbsmpl_seg_metrics = sbsmpl_seg_metrics.clone(prefix="val/")
        self.test_seg_metrics = seg_metrics.clone(prefix="test/")
        self.test_sbsmpl_seg_metrics = sbsmpl_seg_metrics.clone(prefix="test/")

    def configure_optimizers(self) -> Optimizer | dict:
        return self.optim_recipe

    def forward(self, inputs: Tensor) -> Tensor:
        """Forward pass of the model.

        Args:
            inputs (torch.Tensor): Input tensor.
        """
        return self.model(inputs)

    def on_train_start(self) -> None:
        if self.logger is not None:  # coverage: ignore
            self.logger.log_hyperparams(self.hparams)

    def on_validation_start(self) -> None:
        if self.needs_epoch_update and not self.trainer.sanity_checking:
            self.model.update_wrapper(self.current_epoch)
            if hasattr(self.model, "need_bn_update"):
                self.model.bn_update(
                    self.trainer.train_dataloader, device=self.device
                )

    def on_test_start(self) -> None:
        if hasattr(self.model, "need_bn_update"):
            self.model.bn_update(
                self.trainer.train_dataloader, device=self.device
            )

    def training_step(
        self, batch: tuple[Tensor, Tensor], batch_idx: int
    ) -> STEP_OUTPUT:
        img, target = batch
        img, target = self.format_batch_fn((img, target))
        logits = self.forward(img)
        target = F.resize(
            target, logits.shape[-2:], interpolation=F.InterpolationMode.NEAREST
        )
        logits = rearrange(logits, "b c h w -> (b h w) c")
        target = target.flatten()
        valid_mask = target != 255
        loss = self.loss(logits[valid_mask], target[valid_mask])
        if self.needs_step_update:
            self.model.update_wrapper(self.current_epoch)
        self.log("train_loss", loss, prog_bar=True, logger=True)
        return loss

    def validation_step(
        self, batch: tuple[Tensor, Tensor], batch_idx: int
    ) -> None:
        img, targets = batch
        logits = self.forward(img)
        targets = F.resize(
            targets,
            logits.shape[-2:],
            interpolation=F.InterpolationMode.NEAREST,
        )
        logits = rearrange(
            logits, "(m b) c h w -> (b h w) m c", b=targets.size(0)
        )
        probs_per_est = logits.softmax(dim=-1)
        probs = probs_per_est.mean(dim=1)
        targets = targets.flatten()
        valid_mask = targets != 255
        probs, targets = probs[valid_mask], targets[valid_mask]
        self.val_seg_metrics.update(probs, targets)
        self.val_sbsmpl_seg_metrics.update(*self.subsample(probs, targets))

    def test_step(self, batch: tuple[Tensor, Tensor], batch_idx: int) -> None:
        img, targets = batch
        logits = self.forward(img)
        targets = F.resize(
            targets,
            logits.shape[-2:],
            interpolation=F.InterpolationMode.NEAREST,
        )
        logits = rearrange(
            logits, "(m b) c h w -> (b h w) m c", b=targets.size(0)
        )
        probs_per_est = logits.softmax(dim=-1)
        probs = probs_per_est.mean(dim=1)
        targets = targets.flatten()
        valid_mask = targets != 255
        probs, targets = probs[valid_mask], targets[valid_mask]
        self.test_seg_metrics.update(probs, targets)
        self.test_sbsmpl_seg_metrics.update(*self.subsample(probs, targets))

    def on_validation_epoch_end(self) -> None:
        self.log_dict(
            self.val_seg_metrics.compute(), logger=True, sync_dist=True
        )
        self.log(
            "mIoU%",
            self.val_seg_metrics["seg/mIoU"].compute() * 100,
            prog_bar=True,
        )
        self.log_dict(self.val_sbsmpl_seg_metrics.compute(), sync_dist=True)
        self.val_seg_metrics.reset()
        self.val_sbsmpl_seg_metrics.reset()

    def on_test_epoch_end(self) -> None:
        self.log_dict(self.test_seg_metrics.compute(), sync_dist=True)
        self.log_dict(self.test_sbsmpl_seg_metrics.compute(), sync_dist=True)
        if isinstance(self.logger, Logger) and self.log_plots:
            self.logger.experiment.add_figure(
                "Reliabity diagram",
                self.test_sbsmpl_seg_metrics["cal/ECE"].plot()[0],
            )
            self.logger.experiment.add_figure(
                "Risk-Coverage curve",
                self.test_sbsmpl_seg_metrics["sc/AURC"].plot()[0],
            )
            self.logger.experiment.add_figure(
                "Generalized Risk-Coverage curve",
                self.test_sbsmpl_seg_metrics["sc/AUGRC"].plot()[0],
            )

    def subsample(self, pred: Tensor, target: Tensor) -> tuple[Tensor, Tensor]:
        total_size = target.size(0)
        num_samples = max(1, int(total_size * self.metric_subsampling_rate))
        indices = torch.randperm(total_size, device=pred.device)[:num_samples]
        return pred[indices], target[indices]


def _segmentation_routine_checks(
    num_classes: int,
    metric_subsampling_rate: float,
    num_calibration_bins: int,
) -> None:
    if num_classes < 2:
        raise ValueError(f"num_classes must be at least 2, got {num_classes}.")

    if not 0 < metric_subsampling_rate <= 1:
        raise ValueError(
            f"metric_subsampling_rate must be in the range (0, 1], got {metric_subsampling_rate}."
        )

    if num_calibration_bins < 2:
        raise ValueError(
            f"num_calibration_bins must be at least 2, got {num_calibration_bins}."
        )
