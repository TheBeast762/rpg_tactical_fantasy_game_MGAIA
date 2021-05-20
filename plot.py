import matplotlib.pyplot as plt
import json
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot

#
labels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
BAR_WIDTH = 0.05

def read_results(path):
	data = {}
	with open(path) as json_file: 
		data = json.load(json_file)
	return data

def visualize():
	results = read_results('resultsUSER.json')
	ind = np.arange(start=0.1, stop=1.1, step=0.1)
	winRatio = [results[str(label)]['AvgWinRatio'] for label in labels]
	heroStats = [results[str(label)]['AvgHeroStats'] for label in labels]
	foeStats = [results[str(label)]['AvgFoeStats'] for label in labels]

	fig, ax1 = plt.subplots()
	ax1.set_xticks(labels)
	plt.scatter(labels, winRatio, color='seagreen')

	ax1.set_xlabel('Difficulty')
	ax1.set_ylabel('Normalized Win Ratio', color='seagreen')
	ax1.tick_params(axis='y', labelcolor='seagreen')
	ax1.plot(labels, winRatio, color='seagreen')
	ax2 = ax1.twinx()
	ax2.set_ylabel('Avg Cumulative Character Stats', color='purple')

	ax2.bar(ind-BAR_WIDTH/2, heroStats, width=BAR_WIDTH, color='rebeccapurple', label='Protagonists')
	ax2.bar(ind+BAR_WIDTH/2, foeStats, width=BAR_WIDTH, color='fuchsia', label="Foes")
	ax2.tick_params(axis='y', labelcolor='purple')
	#fig.tight_layout()  # otherwise the right y-label is slightly clipped
	ax1.set_zorder(ax2.get_zorder()+1)
	legend = ax2.legend(bbox_to_anchor=(1.08,1), borderaxespad=0)
	ax1.patch.set_visible(False)
	plt.savefig('difficulty_curve.png', 
            dpi=300, 
            format='png', 
            bbox_extra_artists=(legend,), 
            bbox_inches='tight')

visualize()