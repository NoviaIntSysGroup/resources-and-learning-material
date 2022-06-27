# README

**Required python packages to run the accompanying notebooks:**
- numpy,
- matplotlib,
- PyTorch.

## Physics-informed machine learning
Physics informed machine learning was recently reviewed in a Nature reviews [article](https://www.nature.com/articles/s42254-021-00314-5). The concept essentially boils down to embedding known physics into machine learning models, and three potential paths towards accomplishing this goal was presented:
1. **Observational bias:** Use of abundant training data to the degree where one can infer that a trained model will respect the physics as long as it fits the training data.
1. **Inductive bias:** Use taylored network hierarchies (structures) that automatically enforce known physical constraints by design. The best known example in this category is probably convolutional neural networks.
1. **Learning bias:** Modify the loss function so that the network is biased to learn functions that comply with known physical laws during training.

Of the above, the last (learning bias) is the most straight forward to apply, and it has successfully been used to solve differential equations using machine learning. Below, we will summarize this in more detail, and lastly, we end with a field related to physics-informed machine learning "the machine scientist" which can learn the physical laws from raw data.

## Solving differential equations with neural networks
A less well known application of machine learning is in solving differential equations. Such approaches are based on incorporating information about underlying physical laws when training machine learning models (learning bias). The most straight forward examples are physics-informed neural networks (PINNs), which directly include the known physical laws (given as differential equations) into the objective function that is to be minimized during training. This a highly versatile approach for solving differential equations that can seamlessly handle sparse noisy data while also being able to estimate unknown physical parameters (inverse problems). The addition of differential equations (physical laws) to the objective function nonetheless means that one needs to compute derivatives in order to evaluate it. Consequently, the approach relies heavily upon automatic differentiation.

**Literature**
- [Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations](https://www.sciencedirect.com/science/article/pii/S0021999118307125)
- [Physics-informed machine learning](https://www.nature.com/articles/s42254-021-00314-5)

**Blog posts and other online material**
- [Solving differential equations with machine learning](https://medium.com/pasqal-io/solving-differential-equations-with-machine-learning-86bdca8163dc)
- [Introduction to Physics-informed Neural Networks](https://towardsdatascience.com/solving-differential-equations-with-neural-networks-afdcf7b8bcc4)
- [So, what is a physics-informed neural network?](https://benmoseley.blog/my-research/so-what-is-a-physics-informed-neural-network/)

**Physics-informed machine learning software libraries**
- [DeepXDE: PINNs and DeepONets](https://github.com/lululxvi/deepxde)

## Learning operators with neural networks
The standard PINNs can solve a specific differential equation for a specific choice of inputs or initial/border conditions. However, in practice it would be nice to be able to have a network that can solve the differential equation for arbitrary inputs or initial/border conditions. Interestingly, there actually exists a related theorem to the "universal approximation" theorem which states that neural networks can actually accomplish this feat. Based on the general structure of this theorem, the creators of DeepONet designed a network taylored for this task, and also later showed that it could be combined with a "learning bias" to learn to solve differential equations from little or no data for a arbitrary inputs or initial/border conditions.

**Literature**
- [Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators](https://www.nature.com/articles/s42256-021-00302-5)
- [Learning the solution operator of parametric partial differential equations with physics-informed DeepONets](https://www.science.org/doi/10.1126/sciadv.abi8605)

**Blog posts and other online material**
- [Latest Neural Nets Solve World’s Hardest Equations Faster Than Ever Before](https://www.quantamagazine.org/latest-neural-nets-solve-worlds-hardest-equations-faster-than-ever-before-20210419/)

## Machine scientist, learning physical laws from raw data
So far, we have seen that physics-informed machine learning can be used to solve differential equations when the dynamics (equations) are known. However, we don't always know the governing equations, and part of the problem might be to discover these. Machine learning has also impacted the methods that try to solve this different but related problem, and one particular approach uses neural networks (autoencoders) to find the laws directly from raw data. This has even been called "GoPro physics" in cases where the raw data is a video stream.

**Literature**
- [Discovering governing equations from data by sparse identification of nonlinear dynamical systems](https://www.pnas.org/doi/10.1073/pnas.1517384113)
- [Data-driven discovery of coordinates and governing equations](https://www.pnas.org/doi/10.1073/pnas.1906995116)

**Blog posts and other online material**
- [Powerful ‘Machine Scientists’ Distill the Laws of Physics From Raw Data](https://www.quantamagazine.org/machine-scientists-distill-the-laws-of-physics-from-raw-data-20220510/)
- [Sparse Identification of Nonlinear Dynamics (SINDy); YouTube playlist](https://www.youtube.com/watch?v=NxAn0oglMVw&list=PLkjmwL-pF6dzj5aSN2sa4ZNm92G9b4ca2)
