from torch_utils import *
from component import *

# Datasets and Dataloaders
train_data = TripletData(PATH_TRAIN, train_transforms)
val_data = TripletData(PATH_VALID, val_transforms)

train_loader = torch.utils.data.DataLoader(dataset = train_data, batch_size=16, shuffle=True, num_workers=1)
val_loader = torch.utils.data.DataLoader(dataset = val_data, batch_size=16, shuffle=False, num_workers=1)

epochs = 50
device = 'cuda'
best_val_loss = float('inf')
# Our base model
model = models.resnet18().cuda()
optimizer = optim.Adam(model.parameters(), lr=5e-4)
triplet_loss = TripletLoss()
patience_count = 0
stopping_patience = 15

scheduler = ReduceLROnPlateau(optimizer, mode='min',
    factor=0.1, patience=3, threshold=1e-6, threshold_mode='abs', verbose=True)
# Training
for epoch in range(epochs):
    print('Epoch {}/{}'.format(epoch, epochs - 1))
    print('-' * 10)
    model.train()  # Set model to training mode
    train_loss = 0.0
    for data in tqdm(train_loader):
        optimizer.zero_grad()
        x1,x2,x3 = data
        e1 = model(x1.to(device))
        e2 = model(x2.to(device))
        e3 = model(x3.to(device)) 
        
        loss = triplet_loss(e1,e2,e3)
        train_loss += loss
        loss.backward()
        optimizer.step()
    print("Train Loss: {}".format(train_loss.item()))

    model.eval()
    val_loss = 0.0
    for data in tqdm(val_loader):
        optimizer.zero_grad()
        x1,x2,x3 = data
        e1 = model(x1.to(device))
        e2 = model(x2.to(device))
        e3 = model(x3.to(device)) 

        loss = triplet_loss(e1,e2,e3)
        val_loss += loss
    print("Val Loss: {}".format(val_loss.item()))

    scheduler.step(val_loss)

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        print('Model saving......................')
        torch.save(model.state_dict(), '/home/twel/CS232/CBMIR_Res18.pt')
        patience_count = 0
    else:
        patience_count += 1

    if patience_count == stopping_patience:
        break