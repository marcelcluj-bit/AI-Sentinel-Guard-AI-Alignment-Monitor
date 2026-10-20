const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying AIGuardian contract...");

  const AIGuardian = await ethers.getContractFactory("AIGuardian");
  const aiGuardian = await AIGuardian.deploy();

  await aiGuardian.waitForDeployment();

  console.log(`AIGuardian deployed to: ${await aiGuardian.getAddress()}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
