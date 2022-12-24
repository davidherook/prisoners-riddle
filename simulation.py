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

def single_prisoner_attempt(board, prisoner_id):
	success = False
	path_taken = []
	attempts = int(len(board) / 2)
	box_selected = prisoner_id
	for a in range(attempts):
		selection = board[box_selected]
		#print(f"Prisoner: {prisoner_id}; Attempt: {a}; Box Selection: {box_selected}; Result: {selection}")
		path_taken.append(box_selected)
		if selection == prisoner_id:
			success = True
			break
		box_selected = selection
	return success, path_taken

def simulate(n_rounds, n_prisoners):
	prisoners = list(range(1, n_prisoners + 1))
	round_num = []
	prisoners_successful = []
	all_paths_taken = []
	for r in range(n_rounds):
		board = create_board(n_prisoners)
		single_round_result = []
		for prisoner in prisoners:
			result, path_taken = single_prisoner_attempt(board, prisoner)
			single_round_result.append(result)
			all_paths_taken.append([r, prisoner, result, path_taken, len(path_taken)])
		num_prisoners_successful = sum(single_round_result)
		round_num.append(r)
		prisoners_successful.append(num_prisoners_successful)
	df_results = pd.DataFrame({
		'round': round_num,
		'prisoners_successful': prisoners_successful})
	df_paths_taken = pd.DataFrame(
		all_paths_taken,
		columns = ['round', 'prisoner', 'success', 'path_taken', 'path_length'])
	return df_results, df_paths_taken

def save_results(df_results, save_to = None):
	dir_out = 'results'
	if save_to is not None:
		path = os.path.join(dir_out, f"{save_to}_{RUN_TIME}.csv")
	else:
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
	df_results, paths_taken = simulate(rounds, prisoners)
	save_results(df_results)
	save_results(paths_taken, save_to = 'paths_taken')
	print_summary(df_results, rounds, prisoners)
	print(header)

