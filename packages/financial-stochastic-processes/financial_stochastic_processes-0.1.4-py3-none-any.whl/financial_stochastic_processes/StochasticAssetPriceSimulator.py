
import numpy as np

class StochasticAssetPriceSimulator:
    def __init__(self, S0, T, dt, mu=0.05, sigma=0.2, lamb=0.75, p=0.5, lambda1=1.0, lambda2=1.0, kappa=0.15, theta=0.05, xi=0.2, V0=0.05, sigma1=0.2, sigma2=0.2, P_tran=np.array([[0.3,0.7],[0.4,0.6]]),mu_rs=0.07,sigma_rs=0.4, seed=None):
        self.S0 = S0    # Initial stock price        self.S0 = S0    # Initial stock price
        self.T = T      # Time horizon
        self.dt = dt    # Time step size
        self.n_steps = int(self.T / self.dt)  # Number of time steps
        self.mu = mu    # Drift
        self.sigma = sigma  # Volatility (for GBM, Jump Diffusion, Heston)
        self.seed = seed      # Random seed for reproducibility
        
        self.lamb = lamb  # Jump intensity
        self.p = p # Probability for upward jumps
        self.q = 1 - self.p # Probability for downward jumps
        self.lambda1 = lambda1  # λ1 for upward jumps
        self.lambda2 = lambda2  # λ2 for downward jumps
        
        self.kappa = kappa  # Mean reversion rate
        self.theta = theta  # Long-term variance mean
        self.sigma1 = sigma1  # Volatility coefficient for W1
        self.sigma2 = sigma2  # Volatility coefficient for W2

        self.P_tran=P_tran # Transition matrix for regime-switching model
        self.mu_rs=mu_rs # Drift for the second regime
        self.sigma_rs=sigma_rs # Volatility for the second regime
        
        
        
        if seed is not None:
            np.random.seed(seed)

    def simulate_GBM(self): #Monte Carlo Method in FE page 4 1.2
        N = self.n_steps
        t = np.linspace(0, self.T, N+1)
        W = np.random.normal(0, 1, N)
        W = np.cumsum(W) * np.sqrt(self.dt)
        S = self.S0 * np.exp((self.mu - 0.5 * self.sigma ** 2) * t + self.sigma * W)
        return S

    def simulate_jump_diffusion(self): 
#Kou, S.G. (2002) A Jump-Diffusion Model for Option Pricing. 
    #Management Science, 48, 1086-1101. http://dx.doi.org/10.1287/mnsc.48.8.1086.166
        dt = self.dt
        N = self.n_steps
        T = self.T
        t = np.linspace(0, T, N+1)
        S = np.zeros(N+1)
        S[0] = self.S0

        for j in range(1, N+1):
            # Number of jumps in the interval
            k = np.random.poisson(self.lamb * dt)
            # Sum of log jump sizes
            jumps = 0
            if k > 0:
                # Simulate k jump sizes
                U = np.random.uniform(size=k)
                Y = np.where(
                    U < self.p,
                    np.random.exponential(scale=1/self.lambda1, size=k),   # Upward jumps
                    -np.random.exponential(scale=1/self.lambda2, size=k)   # Downward jumps
                )
                jumps = Y.sum()

            # Continuous part
            dW = np.random.normal(0, np.sqrt(dt))
            drift = (self.mu - 0.5 * self.sigma**2) * dt
            diffusion = self.sigma * dW
            S[j] = S[j-1] * np.exp(drift + diffusion + jumps)

        return S

    def simulate_heston(self): # Monte Carlo Method in FE page 356
        # Initialize arrays to store the simulated paths
        S = np.zeros(self.n_steps + 1)
        V = np.zeros(self.n_steps + 1)
        S[0] = self.S0
        V[0] = self.V0

        # Time grid
        t = np.linspace(0, self.T, self.n_steps + 1)

        # Precompute square roots for efficiency
        sqrt_dt = np.sqrt(self.dt)

        for i in range(self.n_steps):
            # Generate independent standard normal random variables
            Delta_W1 = np.random.normal(0, sqrt_dt)
            Delta_W2 = np.random.normal(0, sqrt_dt)
            # Correction term xi (assumed to be zero since not specified)
            xi = 0  # Adjust if xi has a specific definition

            # Ensure variance is non-negative
            V_i = max(V[i], 0)
            sqrt_V_i = np.sqrt(V_i) if V_i > 0 else 0

            # Discretized equations
            # Asset Price
            S_i = S[i]
            if sqrt_V_i > 0:
                term3_S = ((self.mu + (self.sigma1 - self.kappa) / 4) * S_i * sqrt_V_i \
                          + (self.kappa * self.theta / 4 - self.sigma2 ** 2 / 16) * S_i / sqrt_V_i) * Delta_W1 * self.dt
            else:
                term3_S = 0

            term1_S = S_i * (1 + self.mu * self.dt + sqrt_V_i * Delta_W1)
            term2_S = 0.5 * (self.mu ** 2) * S_i * (self.dt ** 2)
            term4_S = 0.5 * S_i * V_i * (Delta_W1 ** 2 - self.dt)
            term5_S = 0.25 * self.sigma2 * S_i * (Delta_W1 * Delta_W2 + xi)

            S[i+1] = term1_S + term2_S + term3_S + term4_S + term5_S

            # Variance
            if sqrt_V_i > 0:
                term4_V = (self.kappa * self.theta / 4 - self.sigma2 ** 2 / 16) / sqrt_V_i
            else:
                term4_V = 0

            term1_V = self.kappa * self.theta * self.dt + (1 - self.kappa * self.dt) * V_i
            term2_V = sqrt_V_i * (self.sigma1 * Delta_W1 + self.sigma2 * Delta_W2)
            term3_V = -0.5 * (self.kappa ** 2) * (self.theta - V_i) * (self.dt ** 2)
            term5_V = -1.5 * self.kappa * sqrt_V_i * (self.sigma1 * Delta_W1 + self.sigma2 * Delta_W2) * self.dt
            term6_V = 0.25 * self.sigma1 ** 2 * (Delta_W1 ** 2 - self.dt)
            term7_V = 0.25 * self.sigma2 ** 2 * (Delta_W2 ** 2 - self.dt)
            term8_V = 0.5 * self.sigma1 * self.sigma2 * Delta_W1 * Delta_W2

            V[i+1] = (term1_V + term2_V + term3_V + term4_V + term5_V + term6_V + term7_V + term8_V)

            # Ensure variance is non-negative
            V[i+1] = max(V[i+1], 0)

        return S, V


    def simulate_regime_switching(self):# invesment gurantees page32
        N = int(self.T / self.dt)
        t = np.linspace(0, self.T, N+1)
        W = np.random.normal(0, 1, N)
        W = np.cumsum(W) * np.sqrt(self.dt)
        S = np.zeros(N)
        S[0] = self.S0
        regime = 0
        regimes=np.array([[self.mu,self.sigma],[self.mu_rs,self.sigma_rs]])
        if np.random.rand()<self.P_tran[regime][0]:
            mu=regimes[regime][0]
            sigma=regimes[regime][1]
        else: 
            regime=1-regime
            mu=regimes[regime][0]
            sigma=regimes[regime][1]
        for i in range(1, N):
            S[i] = S[i-1] * np.exp((mu - 0.5 * sigma ** 2) * self.dt + sigma * W[i])
        return S
