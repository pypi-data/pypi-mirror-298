export async function processVotesAndStakes(
    api: Api,
    votesFor: SS58Address[],
    votesAgainst: SS58Address[],
  ): Promise<VoteWithStake[]> {
    // Get addresses not delegating voting power
    const notDelegatingAddresses = await queryNotDelegatingVotingPower(api);

    // Get stake information
    const { perAddr: stakeFromPerAddr } = await queryStakeFrom(api);
    const { perAddr: stakeOutPerAddr } = await queryStakeOut(api);

    // Function to calculate total stake for an address
    const getTotalStake = (address: SS58Address) => {
      const stakeFrom = stakeFromPerAddr.get(address) ?? 0n;
      const stakeOut = stakeOutPerAddr.get(address) ?? 0n;

      // If the address is staking out to any address but not delegating, return 0
      if (stakeOut > 0n && !notDelegatingAddresses?.includes(address)) {
        return 0n;
      }

      return stakeFrom + stakeOut;
    };

    // Process votes for
    const processedVotesFor = votesFor.map((address) => ({
      address,
      stake: getTotalStake(address),
      vote: "In Favor" as const,
    }));

    // Process votes against
    const processedVotesAgainst = votesAgainst.map((address) => ({
      address,
      stake: getTotalStake(address),
      vote: "Against" as const,
    }));

    // Combine processed votes
    return [...processedVotesFor, ...processedVotesAgainst];
