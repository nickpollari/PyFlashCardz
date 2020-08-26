import ipywidgets
import pandas as pd
import pyflashcards.flashcard as flashcard
import pyflashcards.util as util
import importlib
importlib.reload(flashcard)


# [ ] add validation of csv
# [ ] support tree structure for groups
# [ ] support only looking at certain cards by ID
# [ ] add support for shuffling cards


class Presenter(object):
	def __init__(self, path):
		self._valid_cards = None
		self._valid_groups = dict()
		self.__widgets = dict()
		self.__path = path
		self.__data = self.__load_data(path)

		self.__build_app()

	def get_application(self):
		return self.__widgets['application']
	
	def __build_app(self):
		# build top label
		top_label_html = """
						<font size=1px;!important>
						
						Author: nickpollari@gmail.com
						
						</font>
						"""
		top_label = ipywidgets.HTML(top_label_html)
		group_hbox = self.__widgets['group_hbox']
		# build prev button
		prev_button = self.__build_prev_card_button()
		# build next button
		next_button = self.__build_next_card_button()
		# build card container
		card_container = self.__build_card_container()
		# build card hbox piece
		card_section = ipywidgets.HBox([prev_button,card_container,next_button],
									   layout={'align_items' : 'center',
									   		   'align_content' : 'center'})
		# build the application
		app = ipywidgets.VBox([top_label,group_hbox, card_section])
		self.__widgets['application'] = app

	def __build_card_container(self):
		card = self._valid_cards.next()
		card_container = ipywidgets.VBox([card.get_widget()])
		self.__widgets['card_container'] = card_container
		return card_container

	def __load_data(self, path):
		# load data from path into dataframe
		df = pd.read_csv(path)
		# clean the dataframe
		clean_df = df.dropna(axis=1,how='all').dropna(axis=0,how='all')
		# extract columns
		columns = list(clean_df.columns)
		################################
		######### validate csv #########
		################################

		# create a list to store group checkboxes
		group_checkboxes = list()
		# create a list to container all the cards
		all_cards = list()
		# group the dataframe
		df_gb = clean_df.groupby(columns[0])
		# loop through groups to begin creating cards
		for group, group_df in df_gb:
			# create cards
			cards_map = map(self.__create_card, group_df.iterrows())
			cards = list(cards_map)
			all_cards += cards
			# create group checkbox
			checkbox = self.__build_group_selector(group)
			group_checkboxes.append(checkbox)

		# create group selection section
		self.__build_group_select_box(group_checkboxes)
		# turn valid cards into a cycler
		self._valid_cards = util.bidirectional_iterator(all_cards)

		return clean_df

	def __build_group_select_box(self, group_box_list):
		list_len = len(group_box_list)
		if (list_len % 5) != 0:
			list_len += 5

		iter_list = list(range(0,list_len,5))
		vboxes = list()
		for s_idx, e_idx in zip(iter_list[:-1],iter_list[1:]):
			vbox = ipywidgets.VBox(group_box_list[s_idx:e_idx])
			vboxes.append(vbox)

		# build groups title
		groups_title = ipywidgets.HTML("<b>Groups:<b>")
		vboxes.insert(0,groups_title)
		final_box = ipywidgets.HBox(vboxes)
		self.__widgets['group_hbox'] = final_box

	def __build_group_selector(self, group):
		checkbox = ipywidgets.Checkbox(description=group,
									   value=True,
									   indent=True)
		checkbox.observe(self.__group_checkbox_callback, names=['value'])
		self.__widgets[checkbox._model_id] = checkbox
		self._valid_groups[group] = True
		return checkbox

	def __group_checkbox_callback(self, event):
		group_name = event['owner'].description
		# group_cards = self.cards[group_name]
		self._valid_groups[group_name] = event['new']
		if not any(self._valid_groups.values()):
			event['owner'].unobserve(self.__group_checkbox_callback)
			event['owner'].value = True
			event['owner'].observe(self.__group_checkbox_callback, names=['value'])

	def __create_card(self, row_tuple):
		row_idx, row = row_tuple
		card = flashcard.Flashcard(row['Front'],
								   row['Back'],
								   0,
								   row['Group'])
		return card
		
	def __build_prev_card_button(self):
		btn = ipywidgets.Button(description='',
								button_style='danger',
								icon='arrow-left')
		btn.on_click(self.__prev_next_card_btn_callback)
		self.__widgets['prev_card_btn'] = btn
		return btn

	def __build_next_card_button(self):
		btn = ipywidgets.Button(description='',
								button_style='info',
								icon='arrow-right')
		btn.on_click(self.__prev_next_card_btn_callback)
		self.__widgets['next_card_btn'] = btn
		return btn

	def __prev_next_card_btn_callback(self, btn):
		if btn == self.__widgets['prev_card_btn']:
			iter_func = getattr(self._valid_cards, 'prev')
		else:
			iter_func = getattr(self._valid_cards, 'next')

		while True:
			next_card = iter_func()
			next_card_group = next_card.get_group()
			if self._valid_groups[next_card_group]:
				break

		# get list of current card container children
		curr_children = list(self.__widgets['card_container'].children)
		
		# set this card to be displayed
		curr_children = [next_card.get_widget()]
		self.__widgets['card_container'].children = curr_children
