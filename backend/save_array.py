from torch_utils import *
from component import *
import pickle

load_model = models.resnet18().cuda()
load_model.load_state_dict(torch.load('/home/twel/CS232/model/CBMIR_Res18.pt'))

faiss_index = faiss.IndexFlatL2(1000)   # build the index
collection = []
# storing the image representations
im_indices = []
pred_array = [] #prediction array 
path = (PATH_TRAIN, PATH_VALID)
with torch.no_grad():
    for p in path:
        for f in glob.glob(os.path.join(p, '*/*')):
            im = pil_loader(f)
            im = im.resize((224,224))
            im = torch.tensor([val_transforms(im).numpy()]).cuda()
        
            preds = load_model(im)
            preds = np.array([preds[0].cpu().numpy()])
            pred_array.append(preds)
            # faiss_index.add(preds) #add the representation to index
            im_indices.append(f)   #store the image name to find it later on

for pred in pred_array:
    faiss_index.add(pred)

with open('/home/twel/CS232/backend/array/' + 'faiss_index.pkl', 'wb') as f:
    pickle.dump(faiss_index, f)

with open('/home/twel/CS232/backend/array/' + 'pred_array.pkl', 'wb') as f:
    pickle.dump(pred_array, f)

with open('/home/twel/CS232/backend/array/' + 'im_indices.pkl', 'wb') as f:
    pickle.dump(im_indices, f)
