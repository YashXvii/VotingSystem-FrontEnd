class VotingSystem:
    def __init__(self, candidates):
        self.candidates = candidates
        self.votes = {candidate: 0 for candidate in candidates}

    def display_candidates(self):
        print("Candidates:")
        for candidate in self.candidates:
            print(f"- {candidate}")

    def vote(self, voter_name, selected_candidate):
        if selected_candidate in self.candidates:
            confirm_vote = input(f"Confirm your vote for {selected_candidate} (yes/no): ").lower()
            if confirm_vote == 'yes':
                self.votes[selected_candidate] += 1
                print(f"Vote cast successfully! {voter_name} voted for {selected_candidate}.")
            else:
                print("Vote canceled.")
        else:
            print("Invalid candidate. Please select a valid candidate.")

    def display_results(self):
        print("\nVoting Results:")
        for candidate, votes in self.votes.items():
            print(f"{candidate}: {votes} votes")

if __name__ == "__main__":
    candidates = ["Candidate1", "Candidate2", "Candidate3"]

    # Create a VotingSystem instance
    voting_system = VotingSystem(candidates)

    # Display candidates
    voting_system.display_candidates()

    # Get input from the user
    voter_name = input("\nEnter your name: ")
    selected_candidate = input("Enter the name of the candidate you want to vote for: ")

    # Vote and display results
    voting_system.vote(voter_name, selected_candidate)
    voting_system.display_results()
