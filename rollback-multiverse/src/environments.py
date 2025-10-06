"""
Environment implementations for rollback multiverse experiments.
"""

import numpy as np


class OneHPDuel:
    """
    Minimal environment for the 1 HP double-KO edge case.
    Actions: "attack", "block", "idle".
    """
    
    ACTIONS = ["attack", "block", "idle"]
    
    def __init__(self, seed=None):
        """Initialize the duel environment."""
        self.rng = np.random.RandomState(seed)
        self.reset()
    
    def reset(self):
        """Reset environment to initial state."""
        self.t = 0
        self.hp = 1
        self.done = False
        return self._obs()
    
    def _obs(self):
        """Get current observation."""
        return {"t": self.t, "hp": self.hp, "done": self.done}
    
    def step_resolve(self, a0, a1, arrival0, arrival1):
        """
        Apply actions in canonical order based on arrival timestamps.
        
        Args:
            a0, a1: Actions for players 0 and 1
            arrival0, arrival1: Arrival timestamps
            
        Returns:
            (obs, r0, r1, info) with obs={"t","hp","done"} and info includes order, actions, arrival
        """
        # Determine canonical order (smaller arrival first, tie breaks to player 0)
        if arrival0 <= arrival1:
            first_player, second_player = 0, 1
            first_action, second_action = a0, a1
            first_arrival, second_arrival = arrival0, arrival1
        else:
            first_player, second_player = 1, 0
            first_action, second_action = a1, a0
            first_arrival, second_arrival = arrival1, arrival0
        
        # Resolve actions in canonical order
        r0, r1 = 0, 0
        
        # First player acts
        if first_action == "attack":
            if second_action == "block":
                # Attack blocked, no damage
                pass
            else:
                # Attack hits, second player takes damage
                if second_player == 0:
                    r0 = -1
                else:
                    r1 = -1
        
        # Second player acts (if still alive)
        if second_action == "attack" and (r0 == 0 and r1 == 0):
            if first_action == "block":
                # Attack blocked, no damage
                pass
            else:
                # Attack hits, first player takes damage
                if first_player == 0:
                    r0 = -1
                else:
                    r1 = -1
        
        # Update state
        self.t += 1
        self.hp = 1  # Always 1 HP in this environment
        self.done = (r0 < 0 or r1 < 0)  # Game ends when someone takes damage
        
        info = {
            "order": (first_player, second_player),
            "actions": (a0, a1),
            "arrival": (arrival0, arrival1),
            "canonical_actions": (first_action, second_action)
        }
        
        return self._obs(), r0, r1, info


class GridworldChase:
    """
    Simple gridworld with chaser and runner to extend to spatial dynamics.
    Actions: up, down, left, right, stay.
    """
    
    ACTIONS = ["up", "down", "left", "right", "idle"]
    ACTION_DELTAS = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
        "idle": (0, 0)
    }
    
    def __init__(self, width=5, height=5, seed=None):
        """Initialize the gridworld environment."""
        self.width = width
        self.height = height
        self.rng = np.random.RandomState(seed)
        self.reset()
    
    def reset(self):
        """Reset environment to initial state."""
        # Place chaser and runner at random positions
        self.chaser_pos = (self.rng.randint(0, self.height), self.rng.randint(0, self.width))
        self.runner_pos = (self.rng.randint(0, self.height), self.rng.randint(0, self.width))
        
        # Ensure they're not at the same position
        while self.chaser_pos == self.runner_pos:
            self.runner_pos = (self.rng.randint(0, self.height), self.rng.randint(0, self.width))
        
        self.done = False
        return self._obs()
    
    def _obs(self):
        """Get current observation."""
        return {
            "chaser": self.chaser_pos,
            "runner": self.runner_pos,
            "done": self.done
        }
    
    def step(self, chaser_action, runner_action):
        """
        Update both chaser and runner positions.
        
        Args:
            chaser_action, runner_action: Actions for chaser and runner
            
        Returns:
            (obs, r_chaser, r_runner, info)
        """
        # Apply actions
        self._apply(chaser_action, runner_action)
        
        # Check if caught
        caught = (self.chaser_pos == self.runner_pos)
        self.done = caught
        
        # Rewards: chaser gets +1 for catching, runner gets -1 for being caught
        r_chaser = 1 if caught else 0
        r_runner = -1 if caught else 0
        
        info = {
            "chaser_action": chaser_action,
            "runner_action": runner_action,
            "caught": caught
        }
        
        return self._obs(), r_chaser, r_runner, info
    
    def step_resolve(self, a0, a1, arrival0, arrival1):
        """
        Apply actions in canonical order based on arrival timestamps.
        For GridworldChase, this is the same as step() since order doesn't matter.
        
        Args:
            a0, a1: Actions for players 0 and 1
            arrival0, arrival1: Arrival timestamps
            
        Returns:
            (obs, r0, r1, info) with obs and info includes order, actions, arrival
        """
        # For gridworld, order doesn't matter, so just call step
        obs, r_chaser, r_runner, info = self.step(a0, a1)
        
        # Determine canonical order (smaller arrival first, tie breaks to player 0)
        if arrival0 <= arrival1:
            first_player, second_player = 0, 1
            first_action, second_action = a0, a1
            first_arrival, second_arrival = arrival0, arrival1
        else:
            first_player, second_player = 1, 0
            first_action, second_action = a1, a0
            first_arrival, second_arrival = arrival1, arrival0
        
        # Map rewards to players (assuming player 0 is chaser, player 1 is runner)
        r0, r1 = r_chaser, r_runner
        
        # Add canonical order info
        info.update({
            "order": (first_player, second_player),
            "actions": (a0, a1),
            "arrival": (arrival0, arrival1),
            "canonical_actions": (first_action, second_action)
        })
        
        return obs, r0, r1, info
    
    def _apply(self, chaser_action, runner_action):
        """Apply actions to update positions."""
        # Update chaser position
        delta = self.ACTION_DELTAS[chaser_action]
        new_chaser_pos = (self.chaser_pos[0] + delta[0], self.chaser_pos[1] + delta[1])
        if self._is_valid_pos(new_chaser_pos):
            self.chaser_pos = new_chaser_pos
        
        # Update runner position
        delta = self.ACTION_DELTAS[runner_action]
        new_runner_pos = (self.runner_pos[0] + delta[0], self.runner_pos[1] + delta[1])
        if self._is_valid_pos(new_runner_pos):
            self.runner_pos = new_runner_pos
    
    def _is_valid_pos(self, pos):
        """Check if position is within grid bounds."""
        return 0 <= pos[0] < self.height and 0 <= pos[1] < self.width
