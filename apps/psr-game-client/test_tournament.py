#!/usr/bin/env python3
"""
Basic test script for PSR Game Tournament end-to-end functionality
"""

import sys
import time
import logging
from psr_game_client import PSRGameClient

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_auto_player_registration():
    """Test auto player name generation and registration"""
    logger.info("Testing auto player registration...")
    
    client = PSRGameClient()
    
    # Test auto name generation
    auto_name = client.generate_auto_name()
    if not auto_name:
        logger.error("Failed to generate auto name")
        return False
    
    logger.info(f"Generated auto name: {auto_name}")
    
    # Test registering with auto name
    if not client.register_player(use_auto_name=True):
        logger.error("Failed to register player with auto name")
        return False
    
    logger.info("Auto player registration test passed!")
    return True

def test_bulk_registration():
    """Test bulk player registration for simulation"""
    logger.info("Testing bulk player registration...")
    
    client = PSRGameClient()
    
    # Register 8 players with auto names
    if not client.register_bulk_players(count=8, use_auto_names=True):
        logger.error("Failed to register bulk players")
        return False
    
    # Wait a moment for registration to complete
    time.sleep(2)
    
    # Check tournament state
    state = client.get_tournament_state()
    if not state:
        logger.error("Failed to get tournament state")
        return False
    
    if len(state.get("players", [])) != 8:
        logger.error(f"Expected 8 players, got {len(state.get('players', []))}")
        return False
    
    if state.get("status") != 1:  # Should be InProgress
        logger.error(f"Expected tournament status InProgress (1), got {state.get('status')}")
        return False
    
    logger.info("Bulk player registration test passed!")
    return True

def test_tournament_flow():
    """Test basic tournament flow with referee controls"""
    logger.info("Testing tournament flow...")
    
    client = PSRGameClient()
    
    # Register a player
    if not client.register_player("TestPlayer", use_auto_name=False):
        logger.error("Failed to register test player")
        return False
    
    # Fill the remaining slots with auto players
    if not client.register_bulk_players(count=7, use_auto_names=True):
        logger.error("Failed to register remaining players")
        return False
    
    # Wait for tournament to start
    if not client.wait_for_tournament_start():
        logger.error("Tournament failed to start")
        return False
    
    # Check that we can get tournament state with proper structure
    state = client.get_tournament_state()
    if not state:
        logger.error("Failed to get tournament state")
        return False
    
    required_fields = ["tournamentId", "status", "currentRound", "currentRoundStatus", "players", "matches"]
    for field in required_fields:
        if field not in state:
            logger.error(f"Missing required field in tournament state: {field}")
            return False
    
    logger.info("Tournament flow test passed!")
    return True

def test_api_endpoints():
    """Test that all required API endpoints are accessible"""
    logger.info("Testing API endpoints...")
    
    client = PSRGameClient()
    
    # Test auto name generation endpoint
    auto_name = client.generate_auto_name()
    if not auto_name:
        logger.error("Auto name generation endpoint failed")
        return False
    
    # Test tournament state endpoint
    state = client.get_tournament_state()
    # Note: This might return None if no tournament exists, which is OK
    
    logger.info("API endpoints test passed!")
    return True

def main():
    """Run all tests"""
    logger.info("Starting PSR Game Tournament tests...")
    
    tests = [
        ("Auto Player Registration", test_auto_player_registration),
        ("API Endpoints", test_api_endpoints),
        ("Bulk Registration", test_bulk_registration),
        ("Tournament Flow", test_tournament_flow),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running test: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            if test_func():
                logger.info(f"✅ {test_name} PASSED")
                passed += 1
            else:
                logger.error(f"❌ {test_name} FAILED")
                failed += 1
        except Exception as e:
            logger.error(f"❌ {test_name} FAILED with exception: {e}")
            failed += 1
        
        # Wait between tests to avoid conflicts
        time.sleep(3)
    
    logger.info(f"\n{'='*50}")
    logger.info(f"Test Results: {passed} passed, {failed} failed")
    logger.info(f"{'='*50}")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)