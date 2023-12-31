import sys
import os
curPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(curPath)
print("当前的工作目录：",os.getcwd())
print("python搜索模块的路径集合",sys.path)
import openke
from openke.config import Trainer, Tester
from openke.module.model import TransE
from openke.module.loss import MarginLoss
from openke.module.strategy import NegativeSampling
from openke.data import TrainDataLoader, TestDataLoader

# dataloader for training
train_dataloader = TrainDataLoader(
	in_path = "../benchmarks/KGC/",
	nbatches = 100,
	threads = 8,
	sampling_mode = "normal",
	bern_flag = 1,
	filter_flag = 1,
	neg_ent = 25,
	neg_rel = 0)

# dataloader for test
# test_dataloader = TestDataLoader("../benchmarks/FB15K237/", "link")

# define the model
transe = TransE(
	ent_tot = train_dataloader.get_ent_tot(),
	rel_tot = train_dataloader.get_rel_tot(),
	dim = 1024,
	p_norm = 1,
	norm_flag = True)


# define the loss function
model = NegativeSampling(
	model = transe,
	loss = MarginLoss(margin = 5.0),
	batch_size = train_dataloader.get_batch_size()
)

# train the model
trainer = Trainer(model = model, data_loader = train_dataloader, train_times = 100, alpha = 1.0, use_gpu = True)
trainer.run()
transe.save_checkpoint('../checkpoint/transe.ckpt')

# test the model
# transe.load_checkpoint('../checkpoint/transe.ckpt')
# tester = Tester(model = transe, data_loader = test_dataloader, use_gpu = True)
# tester.run_link_prediction(type_constrain = False)


import pickle
ent_embeddings = transe.ent_embeddings.weight.data.cpu().detach().numpy()
rel_embeddings = transe.rel_embeddings.weight.data.cpu().detach().numpy()
pickle.dump(ent_embeddings, open("../res//ent_embeddings","wb"))
pickle.dump(rel_embeddings, open("../res//rel_embeddings","wb"))