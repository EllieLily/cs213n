# user define model of pic captioning

# As usual, a bit of setup

import time, os, json
import numpy as np
import matplotlib.pyplot as plt

from cs231n.captioning_solver import CaptioningSolver
from cs231n.coco_utils import load_coco_data, sample_coco_minibatch, decode_captions
from cs231n.gradient_check import eval_numerical_gradient, eval_numerical_gradient_array
# from cs231n.image_utils import image_from_url
from cs231n.rnn_layers import *
from cs231n.classifiers.rnn import CaptioningRNN

small_data2 = load_coco_data(max_train=500)  # test

# Load COCO data from disk; this returns a dictionary
# We'll work with dimensionality-reduced features for this notebook, but feel
# free to experiment with the original features by changing the flag below.
data = load_coco_data(pca_features=True)
# Print out all the keys and values from the data dictionary
for k, v in data.iteritems():
    if type(v) == np.ndarray:
        print k, type(v), v.shape, v.dtype
    else:
        print k, type(v), len(v)

# Look at the sample data, have a sense of dataset
# Sample a minibatch and show the images and captions
batch_size = 3

captions, features, urls = sample_coco_minibatch(data, batch_size=batch_size)
for i, (caption, url) in enumerate(zip(captions, urls)):
  # plt.imshow(image_from_url(url))
  plt.axis('off')
  caption_str = decode_captions(caption, data['idx_to_word'])
  plt.title(caption_str)
  plt.show()

# Train a good captioning model!
# To relieve overfitting, did:
# (1) incrase max_train from 50 to 500
# (2) decrease num_epoches from 50 to 25

good_model = CaptioningRNN(
    cell_type='lstm',
    word_to_idx=data['word_to_idx'],
    input_dim=data['train_features'].shape[1],
    hidden_dim=512,
    wordvec_dim=256,
    dtype=np.float32,
)

good_solver = CaptioningSolver(good_model, small_data2,
                               update_rule='adam',
                               num_epochs=25,
                               batch_size=25,
                               optim_config={
                                   'learning_rate': 5e-3,
                               },
                               lr_decay=0.995,
                               verbose=True, print_every=50,
                               )

good_solver.train()

# Plot the training losses
plt.plot(good_solver.loss_history)
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.title('Training loss history')
plt.show()

# Notify when finished
from IPython.display import Audio

sound_file = './sound/finish.mp3'
Audio(url=sound_file, autoplay=True)

for split in ['train', 'val']:
  minibatch = sample_coco_minibatch(small_data2, split=split, batch_size=2)
  gt_captions, features, urls = minibatch
  gt_captions = decode_captions(gt_captions, data['idx_to_word'])

  sample_captions = good_model.sample(features)
  sample_captions = decode_captions(sample_captions, data['idx_to_word'])

  for gt_caption, sample_caption, url in zip(gt_captions, sample_captions, urls):
    # plt.imshow(image_from_url(url))
    plt.title('%s\n%s\nGT:%s' % (split, sample_caption, gt_caption))
    plt.axis('off')
    plt.show()