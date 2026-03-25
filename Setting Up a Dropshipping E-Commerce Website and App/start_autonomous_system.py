#!/usr/bin/env python3
"""
Alpapies Autonomous Agent System Startup
Launches all autonomous agents to run the business automatically
"""

import asyncio
import signal
import sys
import os
from autonomous_agent_core import AutonomousAgentManager, DesignOptimizationAgent, ProductResearchAgent, PricingOptimizationAgent, MarketingAutomationAgent

class AlpapiesAutonomousSystem:
    """Main system controller for autonomous business operations"""
    
    def __init__(self):
        self.manager = AutonomousAgentManager()
        self.setup_agents()
        self.setup_signal_handlers()
        
    def setup_agents(self):
        """Setup all autonomous agents"""
        print("🤖 ALPAPIES AUTONOMOUS BUSINESS SYSTEM")
        print("=" * 60)
        print("🚀 Initializing world-class autonomous agents...")
        
        # Register all autonomous agents
        agents = [
            DesignOptimizationAgent(),
            ProductResearchAgent(), 
            PricingOptimizationAgent(),
            MarketingAutomationAgent()
        ]
        
        for agent in agents:
            self.manager.register_agent(agent)
            print(f"✅ {agent.name} Agent: {', '.join(agent.capabilities)}")
        
        print(f"\n🎯 {len(agents)} autonomous agents ready for deployment")
        print("💡 These agents will continuously improve your business 24/7")
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down autonomous agents...")
        asyncio.create_task(self.manager.stop_all_agents())
        sys.exit(0)
        
    async def start(self):
        """Start the autonomous system"""
        print("\n🚀 LAUNCHING AUTONOMOUS BUSINESS OPERATIONS")
        print("=" * 60)
        print("⚡ Agents will now work continuously to:")
        print("   • Optimize website design and UX")
        print("   • Research and add new products from 1688.com")
        print("   • Optimize pricing for maximum profit")
        print("   • Create and deploy marketing campaigns")
        print("   • Monitor competitors and market trends")
        print("   • Improve conversion rates and performance")
        print("\n🎯 Your business is now running autonomously!")
        print("📊 Monitor progress in the logs and dashboard")
        print("=" * 60)
        
        # Start all agents
        await self.manager.start_all_agents()

def main():
    """Main entry point"""
    # Ensure we're in the right directory
    os.chdir('/home/ubuntu/alpapies-complete-project')
    
    # Create and start the autonomous system
    system = AlpapiesAutonomousSystem()
    
    try:
        asyncio.run(system.start())
    except KeyboardInterrupt:
        print("\n✅ Autonomous system shutdown complete")
    except Exception as e:
        print(f"❌ Error in autonomous system: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

