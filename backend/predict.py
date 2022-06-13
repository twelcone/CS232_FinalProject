import pickle
from component import *

with open('./backend/array/' + 'pred_array.pkl', 'rb') as f:
    pred_array = pickle.load(f)
with open('./backend/array/' + 'faiss_index.pkl', 'rb') as f:
    faiss_index = pickle.load(f)
with open('./backend/array/' + 'im_indices.pkl', 'rb') as f:
    im_indices = pickle.load(f)

load_model = models.resnet18().cuda()
load_model.load_state_dict(torch.load('./backend/CBMIR_Res18.pt'))

def read_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return image.convert('RGB')

def get_prediction(image_bytes):
    with torch.no_grad():
        im = read_image(image_bytes)
        im = im.resize((224,224))
        im = torch.tensor([val_transforms(im).numpy()]).cuda()
    
        test_embed = load_model(im).cpu().numpy()
        _, I = faiss_index.search(test_embed, 15)
        # print("Retrieved Image: {}".format(im_indices[I[0][0]]))
        predict = []
        for i in range(15):
            predict.append(im_indices[I[0][i]])
        return predict

def get_prediction_imgPATH(file):
    with torch.no_grad():
        im = pil_loader(file)
        im = im.resize((224,224))
        im = torch.tensor([val_transforms(im).numpy()]).cuda()
    
        test_embed = load_model(im).cpu().numpy()
        _, I = faiss_index.search(test_embed, 15)
        # print("Retrieved Image: {}".format(im_indices[I[0][0]]))
        predict = []
        for i in range(15):
            predict.append(im_indices[I[0][i]])
        return predict

if __name__ == '__main__':
    a = get_prediction_imgPATH('/home/twel/CS232/backend/test/brain_007.png')
    print(a)
