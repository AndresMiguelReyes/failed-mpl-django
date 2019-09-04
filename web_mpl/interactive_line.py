import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('WebAgg')


class InteractiveLine:
	def __init__(self, points_list, fig):
		self.fig = fig
		self.fig.add_subplot(111)
		self.ax = self.fig.axes[0]
		self.tolerance = 10
		self.xy = points_list

		x_data = [pt[0] for pt in points_list]
		y_data = [pt[1] for pt in points_list]
		# #39ff14
		self.points = self.ax.scatter(
			x_data, y_data, s=200, color='#ff00ff',
			picker=self.tolerance, zorder=1)
		self.line = self.ax.plot(
			x_data, y_data, ls='--', c='#666666',
			zorder=0)

		# test_cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

	def on_click(self, event):
		contains, info = self.points.contains(event)
		print(contains)
		print(info)
		if contains:
			ind = info['ind'][0]
			print("You clicked {}!".format(ind))
			self.start_drag(ind)

	def start_drag(self, ind):
		self.drag_ind = ind
		connect = self.fig.canvas.mpl_connect
		cid1 = connect('motion_notify_event', self.drag_update)
		cid2 = connect('button_release_event', self.end_drag)
		self.drag_cids = [cid1, cid2]
		self.on_press()

	def drag_update(self, event):
		self.xy[self.drag_ind] = [event.xdata, event.ydata]
		self.points.set_offsets(self.xy)
		self.ax.draw_artist(self.points)
		self.fig.canvas.draw()

	def end_drag(self, event):
		"""End the binding of mouse motion to a particular point."""
		self.redraw()
		for cid in self.drag_cids:
			self.fig.canvas.mpl_disconnect(cid)

	def on_press(self):
		self.line[0].set_alpha(.4)

	def redraw(self):
		x_data, y_data = self.line[0].get_data()
		pt_x, pt_y = self.xy[self.drag_ind]
		x_data[self.drag_ind] = pt_x
		y_data[self.drag_ind] = pt_y
		self.line[0].set_data(x_data,y_data)
		self.line[0].set_alpha(1)
		self.fig.canvas.draw()


	def setup_axes(self):
		fig, ax = plt.subplots(num="test")
		return fig, ax

	def show(self):
		plt.show()