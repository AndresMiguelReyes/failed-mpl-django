import asyncio
import base64
import inspect
import json
import matplotlib.pyplot as plt
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .interactive_line import InteractiveLine


class MplConsumer(AsyncConsumer):
	supports_binary = True

	async def websocket_connect(self, event):
		print("connected", event)
		fig_id = self.scope['url_route']['kwargs']['fig_id']

		self.figure = plt.figure(num="test")
		point_coords = [[.75, .75],
						[1, 1],
						[1.25, .125]]
		self.il = InteractiveLine(point_coords,self.figure)
		self.content_to_send = None
		plt.savefig('fig_at_consumer.png')
		# self.figure = il.fig
		# self.manager = self.figure.canvas.manager
		self.il.fig.canvas.manager.add_web_socket(self)
		self.il.fig.canvas.mpl_connect('button_press_event', self.on_click)

		await self.send({
			"type": "websocket.accept"
		})

	def send_json(self, content):
		self.content_to_send = {
			'type': 'text',
			'content': json.dumps(content),
		}
		# await self.send(json.dumps(content))

	def send_binary(self, blob):
		if self.supports_binary:
			self.content_to_send = {
				'type': 'bytes',
				'content': blob,
			}
		else:
			# b64_blob = str(blob).replace('\n', '')
			# data_uri = "data:image/png;base64,{0}".format(b64_blob)
			# self.content_to_send = {
			# 	'type': 'text',
			# 	'content': data_uri,
			# }
			self.content_to_send = {
				'type': 'bytes',
				'content': blob,
			}

	async def websocket_receive(self, event):
		# print("receive", event)
		message = json.loads(event['text'])
		if message['type'] == 'supports_binary':
			self.supports_binary = message['value']
		else:
			self.il.fig.canvas.manager.handle_json(message)

		if self.content_to_send is not None:
			content_dict = {
				"type": "websocket.send",
				self.content_to_send['type']: self.content_to_send['content'],
			}
			# print("Sending...",content_dict)
			await self.send(content_dict)

	async def websocket_disconnect(self, event):
		print("disconnected", event)

	def on_click(self, event):
		contains, info = self.il.points.contains(event)
		print(contains)
		print(info)
		if contains:
			ind = info['ind'][0]
			print("You clicked {}!".format(ind))
			self.start_drag(ind)

	def start_drag(self, ind):
		self.drag_ind = ind
		connect = self.il.fig.canvas.mpl_connect
		cid1 = connect('motion_notify_event', self.drag_update)
		cid2 = connect('button_release_event', self.end_drag)
		self.il.drag_cids = [cid1, cid2]
		self.on_press()

	def drag_update(self, event):
		self.il.xy[self.drag_ind] = [event.xdata, event.ydata]
		self.il.points.set_offsets(self.il.xy)
		self.il.ax.draw_artist(self.il.points)
		self.il.fig.canvas.draw()

	def end_drag(self, event):
		"""End the binding of mouse motion to a particular point."""
		print("going to redraw!")
		self.redraw()
		for cid in self.il.drag_cids:
			self.il.fig.canvas.mpl_disconnect(cid)

	def on_press(self):
		self.il.line[0].set_alpha(.4)

	def redraw(self):
		x_data, y_data = self.il.line[0].get_data()
		pt_x, pt_y = self.il.xy[self.drag_ind]
		x_data[self.drag_ind] = pt_x
		y_data[self.drag_ind] = pt_y
		self.il.line[0].set_data(x_data, y_data)
		self.il.line[0].set_alpha(1)
		self.il.fig.savefig('r.png')
		self.il.fig.canvas.draw()
		self.il.fig.savefig('r2.png')