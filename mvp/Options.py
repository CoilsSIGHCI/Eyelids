class PresetOptionsResNetL:
    def __init__(self, pretrain_path, model, width_mult, root_path="~/", video_path="~/datasets/EgoGesture",
                 annotation_path="Real-time-GesRec-2/annotation_EgoGesture/egogestureall_but_None.json",
                 result_path="Real-time-GesRec-2/results", dataset="egogesture", n_classes=27, n_finetune_classes=83,
                 model_depth=10, resnet_shortcut="B", resnext_cardinality=16, train_crop="random", learning_rate=0.01,
                 sample_size=112, sample_duration=32, modality="Depth", pretrain_modality="RGB", downsample=1, batch_size=24,
                 n_threads=16, checkpoint=1, n_val_samples=1, n_epochs=60, ft_portion="complete", no_train=True,
                 no_val=False, test=False, resume_path=None, test_subset=None, no_cuda=True):
        self.root_path = root_path
        self.video_path = video_path
        self.annotation_path = annotation_path
        self.result_path = result_path
        self.pretrain_path = pretrain_path
        self.dataset = dataset
        self.n_classes = n_classes
        self.n_finetune_classes = n_finetune_classes
        self.model = model
        self.width_mult = width_mult
        self.model_depth = model_depth
        self.resnet_shortcut = resnet_shortcut
        self.resnext_cardinality = resnext_cardinality
        self.train_crop = train_crop
        self.learning_rate = learning_rate
        self.sample_size = sample_size
        self.sample_duration = sample_duration
        self.modality = modality
        self.pretrain_modality = pretrain_modality
        self.downsample = downsample
        self.batch_size = batch_size
        self.n_threads = n_threads
        self.checkpoint = checkpoint
        self.n_val_samples = n_val_samples
        self.n_epochs = n_epochs
        self.ft_portion = ft_portion
        self.no_train = no_train
        self.no_val = no_val
        self.test = test
        self.resume_path = resume_path
        self.test_subset = test_subset
        self.no_cuda = no_cuda


class PresetOptions1:
    def __init__(self, pretrain_path, model, width_mult, root_path="~/", video_path="~/datasets/EgoGesture",
                 annotation_path="Real-time-GesRec-2/annotation_EgoGesture/egogestureall_but_None.json",
                 result_path="Real-time-GesRec-2/results", dataset="egogesture", n_classes=27, n_finetune_classes=83,
                 model_depth=10, resnet_shortcut="B", resnext_cardinality=16, train_crop="random", learning_rate=0.01,
                 sample_size=112, sample_duration=32, modality="Depth", pretrain_modality="RGB", downsample=1, batch_size=24,
                 n_threads=16, checkpoint=1, n_val_samples=1, n_epochs=60, ft_portion="complete", no_train=False,
                 no_val=False, test=False, resume_path=None, test_subset=None, no_cuda=True):
        self.root_path = root_path
        self.video_path = video_path
        self.annotation_path = annotation_path
        self.result_path = result_path
        self.pretrain_path = pretrain_path
        self.dataset = dataset
        self.n_classes = n_classes
        self.n_finetune_classes = n_finetune_classes
        self.model = model
        self.width_mult = width_mult
        self.model_depth = model_depth
        self.resnet_shortcut = resnet_shortcut
        self.resnext_cardinality = resnext_cardinality
        self.train_crop = train_crop
        self.learning_rate = learning_rate
        self.sample_size = sample_size
        self.sample_duration = sample_duration
        self.modality = modality
        self.pretrain_modality = pretrain_modality
        self.downsample = downsample
        self.batch_size = batch_size
        self.n_threads = n_threads
        self.checkpoint = checkpoint
        self.n_val_samples = n_val_samples
        self.n_epochs = n_epochs
        self.ft_portion = ft_portion
        self.no_train = no_train
        self.no_val = no_val
        self.test = test
        self.resume_path = resume_path
        self.test_subset = test_subset
        self.no_cuda = no_cuda
