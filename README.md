# THORChain-Fee-Calculator
### THORChain
THORChain is a protocol that allows users to swap native assets without an intermediary of a centralized exchange. Until now, a user had to sign up with an exchange and complete KYC procedures to trade native assets like, for example, Bitcoin and Litecoin. Previous approaches to this challenge, like Wrapping and Atomic Swaps, didn't achieve the goal of creating a trustless exchange or have been largely illiquid.

### Fees
Fees on THORChain are divided into four categories, from which one or more can be present in each transaction: network fees, native asset transaction fees, slip fees, and affiliate fees. In a swap, these fees are deducted from the inbound or outbound asset automatically and do not require the user to hold any RUNE, simplifying the user experience.

The Network fee is a flat fee that the user pays for any transaction involving the THORChain network. The Network fee is fixed at 0.02 RUNE and is subtracted automatically from the user's balance or the payment. In the event of a swap where the user does not own any RUNE, the Network fee is subtracted from the inbound asset in the asset's currency.

The Network fee from each transaction automatically gets added to the Liquidity Emission Reserve. The reserve currently contains approximately 190 million RUNE and distributes 1/6 of the balance annually to Validating Nodes and Liquidity Providers in a ratio determined by the Incentive Pendulum. This distribution comes once per block. Nodes and Liquidity Providers receive 100% of the Slip fees paid by users and the Block Reward that comes from the reserve.

Native asset fees are used to pay inbound and outbound transaction fees on native blockchains such as Bitcoin, Ethereum, and Litecoin. The price for sending tokens into and from THORChain Vaults is calculated from the runtime gas fees of both the inbound and outbound assets.

Slip fees are the penalty for shifting the price in the AMM liquidity pool. Slip fees are unique to the THORChain platform and were conceived to allow the network to prioritize large transactions and prevent frontrunning. These fees are calculated as the percentage of the liquidity pool of the inbound asset which the swap constitutes. For a doubleswap, the slip-based fee is applied twice.

Finally, affiliate fees allow ecosystem developers to benefit from the utilization of their front-end applications. Affiliate fees can be of any amount and are added to the memo of the transaction. Like the network fee, if the user does not own any RUNE, the fee is subtracted from the inbound asset.

Because the swap fees contain both fixed and variable components, there remains an area for execution optimization. A large trade can be broken down into smaller transactions to reduce the Slip fee and increase the output value received from the swap. For example, for the transaction shown above, if the trade is split into two swaps of 0.5 BTC, the user will pay twice as much fixed fees, but the total Slip fee will be reduced by approximately 50%. For the first swap (BTC to RUNE), the user will pay roughly $105. Similarly, for the second swap, the user will pay $133 (the fee is higher here because the ETH-RUNE pool has less liquidity, and thus the price impact is higher).

### Fee Optimization Calculator
We saw this opportunity for optimization of transaction fees and developed a simple algorithm that allows users to find out in how many swaps they should split their trade on THORChain to minimize the associated costs.

This python script allows users to input specifics of their trade and the THORChain pools which their transaction will involve. Upon completion of these inputs and after a subsequent calculation, the script will output the optimal number of transactions and the minimized estimated transaction costs.

### Further Development
Our fee optimization calculator by no means provides the optimal user experience. We encourage developers from the THORChain community to help us tackle the challenge of allowing users to minimize transaction costs by building a GUI around the script we created. Further improvements may include automated input of THORChain pool liquidity, an online UX, and even an automated execution of the split-up trade.

We look forward to seeing THORChain develop and hope that this calculator will provide value to the community and serve as a valuable addition to the THORChain ecosystem.
