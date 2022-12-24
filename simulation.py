import os
import time
import random
import argparse
import pandas as pd

RUN_TIME = int(time.time())

def create_board(prisoners):
	board = {}
	boxes = list(range(1, prisoners + 1))
	papers = list(range(1, prisoners + 1))
	random.shuffle(papers)
	for b in boxes:
		board[b] = papers[b - 1]
	return board

def is_correct(selection, prisoner_id):
	if selection == prisoner_id:
		return True
	return False

def single_prisoner_attempt(board, prisoner_id):
	success = False
	attempts = int(len(board) / 2)
	box_selected = prisoner_id
	for a in range(attempts):
		selection = board[box_selected]
		#print(f"Prisoner: {prisoner_id}; Attempt: {a}; Box Selection: {box_selected}; Result: {selection}")
		if is_correct(selection, prisoner_id):
			success = True
			break
		box_selected = selection
	return success

def simulate(n_rounds, n_prisoners):
	prisoners = list(range(1, n_prisoners + 1))
	round_num = []
	prisoners_successful = []
	for r in range(n_rounds):
		board = create_board(n_prisoners)
		single_round_result = []
		for prisoner in prisoners:
			result = single_prisoner_attempt(board, prisoner)
			single_round_result.append(result)
		num_prisoners_successful = sum(single_round_result)
		round_num.append(r)
		prisoners_successful.append(num_prisoners_successful)
	return pd.DataFrame({
		'round': round_num,
		'prisoners_successful': prisoners_successful})

def save_results(df_results):
	dir_out = 'results'
	path = os.path.join(dir_out, f"results_{RUN_TIME}.csv")
	if not os.path.isdir(dir_out):
		os.mkdir(dir_out)
	df_results.to_csv(path, index = False)
	print(f"Saved results to {path}")

def print_summary(df_results, rounds, prisoners):
	filter_success = df_results['prisoners_successful'] == prisoners
	successful_rounds = df_results[filter_success].shape[0]
	results = {
		'Prisoners per Round': prisoners,
		'Rounds Simulated': rounds,
		'Rounds Successful': successful_rounds,
		'% Success': successful_rounds / rounds
	}
	print('\nResults Summary:\n')
	for k,v in results.items():
		print(k, v)

if __name__ == '__main__':
	header = '\n' + '*' * 50 + '\n'
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--rounds', type = int, help = 'The number of rounds to simulate')
	parser.add_argument('-p', '--prisoners', type = int, help = 'The number of prisoners')
	args = vars(parser.parse_args())
	rounds = args['rounds']
	prisoners = args['prisoners']

	print(header)
	print(f"Simulating {rounds} rounds with {prisoners} prisoners each round...")
	df_results = simulate(rounds, prisoners)
	save_results(df_results)
	print_summary(df_results, rounds, prisoners)
	print(header)

