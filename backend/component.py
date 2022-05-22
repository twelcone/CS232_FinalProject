from torch_utils import *

PATH_TRAIN = '/home/twel/CS232/dataset/train'
PATH_VALID = '/home/twel/CS232/dataset/val'
PATH_TEST = '/home/twel/CS232/dataset/test'

def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('RGB')

class TripletLoss(nn.Module):
    def __init__(self, margin=1.0):
        super(TripletLoss, self).__init__()
        self.margin = margin
        
    def calc_euclidean(self, x1, x2):
        return (x1 - x2).pow(2).sum(1)
    
    # Distances in embedding space is calculated in euclidean
    def forward(self, anchor, positive, negative):
        distance_positive = self.calc_euclidean(anchor, positive)
        distance_negative = self.calc_euclidean(anchor, negative)
        losses = torch.relu(distance_positive - distance_negative + self.margin)
        return losses.mean()

class TripletData(Dataset):
    def __init__(self, path, transforms, split="train"):
        self.path = path
        self.split = split    # train or valid
        self.num_cats = 7       # number of categories
        self.transforms = transforms
        self.cats = sorted(os.listdir(path))
    
    def __getitem__(self, idx):
        # our positive class for the triplet
        idx = idx%self.num_cats 
        # print(idx)
        # print(self.path)
        # choosing our pair of positive images (im1, im2)
        positives = os.listdir(os.path.join(self.path, self.cats[idx]))
        im1, im2 = random.sample(positives, 2)
        
        # choosing a negative class and negative image (im3)
        negative_cats = [x for x in range(self.num_cats)]
        negative_cats.remove(idx)
        negative_cat = random.choice(negative_cats)
        negatives = os.listdir(os.path.join(self.path, self.cats[negative_cat]))
        im3 = random.choice(negatives)
        
        im1,im2,im3 = os.path.join(self.path, self.cats[idx], im1), os.path.join(self.path, self.cats[idx], im2), os.path.join(self.path, self.cats[negative_cat], im3)
    
        im1 = self.transforms(pil_loader(im1))
        im2 = self.transforms(pil_loader(im2))
        im3 = self.transforms(pil_loader(im3))
        
        return [im1, im2, im3]
        
    # we'll put some value that we want since there can be far too many triplets possible
    # multiples of the number of images/ number of categories is a good choice
    def __len__(self):
        return self.num_cats*8


# Transforms
train_transforms = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
   transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
   transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])
