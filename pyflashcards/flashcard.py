import ipywidgets

# [ ] support themes via layout_obj


class Flashcard(object):
    def __init__(self, front_text, back_text, card_id, group, layout_obj=None):
        self.__front_text = front_text
        self.__back_text = back_text
        self.__id = card_id
        self.__group = group
        self.__layout_obj = layout_obj  # to be used in the future to support themes
        self.__widgets = dict()
        self.__displayed_side = 'Front'

        # build the card
        self.__build_card()

    def get_group(self):
        return self.__group

    def get_widget(self):
        """
        Used as only public method
        to get the card widget object

        Returns:
            card_widget (ipywidgets.VBox)
        """
        card_widget = self.__widgets['card']
        return card_widget

    def __set_card_side_text(self, side_text):
        """
        Sets the value of the 'card_side'
        widget with relevant HTML

        Parameters:
            side_text (str): 'Front' or 'Back'
        """
        side_html = """
                    <p style="font-size: 12px;
                              text-align: right;
                              padding-right: 5px;">
                    <b>Card Side:</b> {text}
                    </p>
                    """.format(text=side_text)

        self.__widgets['card_side'].value = side_html
        self.__displayed_side = side_text

    def __build_card_side_widget(self, side_text):
        """
        Builds the card side being displayed
        widget to show user if they are
        looking at the front or back
        of a card

        Parameters:
            side_text (str): 'Front' or 'Back'

        Returns:
            side_shown (ipywidgets.HTML)
        """
        # build the widget
        side_shown = ipywidgets.HTML("")
        # save the widget
        self.__widgets['card_side'] = side_shown
        # set the value of the side shown
        self.__set_card_side_text(side_text)
        return side_shown

    def __build_card(self):
        """
        Primary function which builds the
        actual card GUI that is displayed
        to users
        """
        # build the group widget
        group = self.__build_card_group_widget()
        # build the front of the card
        card_front = self.__build_face_of_card(self.__front_text)
        self.__widgets['card_front'] = card_front
        # build the back of the card
        card_back = self.__build_face_of_card(self.__back_text)
        self.__widgets['card_back'] = card_back
        # build a box to contain the card face being shown
        card_face = ipywidgets.VBox([card_front],
                                    layout={'min_width' : '350px',
                                            'min_height' : '150px',
                                            'border' : '2px solid black'})
        self.__widgets['card_face'] = card_face
        # build a widget to show what side
        # of the card is being displayed
        side_shown = self.__build_card_side_widget(self.__displayed_side)
        # build a widget to display
        # the id of the card
        card_id = self.__build_id_widget()
        # build a button to flip the card
        # between front and back text
        flip_button = self.__build_flip_card_button()
        # build a box for the button so we can adjust
        # where in the box the button shows up
        button_box = ipywidgets.VBox([flip_button],
                                    layout={'align_content' : 'center',
                                             'align_items' : 'center',
                                             'justify_content' : 'center',
                                             'justify_items' : 'center'})

        # vertically stack the group, side_shown,
        # card_face, and card_id widgets
        card = ipywidgets.VBox([group, side_shown,
                                card_face, card_id, button_box])

        # store this in widgets to be retrieved later
        self.__widgets['card'] = card

    def __build_card_group_widget(self):
        """
        Builds a widget to display what group
        this flashcard question belongs to

        Returns:
            group_widget (ipywidget.HTML)
        """
        # check whether group exists
        if self.__group is None:
            group_name = ""
        else:
            group_name = str(self.__group)
        # html to display group name
        group_html = """
                     <p style="font-size: 12px;
                               padding-left: 5px;">
                     <b>Card Group:</b> {text}
                     </p>
                     """.format(text=group_name)
        # widget for displaying group name
        group_widget = ipywidgets.HTML(group_html)
        # save the widget
        self.__widgets['card_group'] = group_widget
        return group_widget

    def __build_face_of_card(self, text):
        """
        Builds a widget to display text
        on one side of the card. To be used
        to build the front and back of a 
        given card

        Parameters:
            text (str): text to display on the card

        Returns:
            text_widget (ipywidgets.HTML)
        """
        # ensure text is actually a str
        clean_text = str(text)
        # create a widget for front/back of card
        text_widget = ipywidgets.HTML(clean_text, layout={'border' : '3px solid orange',
                                                          'min_height' : '95%'})
        return text_widget

    def __build_id_widget(self):
        """
        Builds a widget to display the card ID

        Returns:
            id_widget (ipywidgets.HTML)
        """
        id_html = """
                  <p style="font-size: 12px;
                            padding-left: 5px;">
                  <b>Card ID: </b>{id_text}
                  </p>
                  """.format(id_text=self.__id)
        id_widget = ipywidgets.HTML(id_html)
        self.__widgets['card_id'] = id_widget
        return id_widget

    def __build_flip_card_button(self):
        """
        Builds a button to be used to flip
        the card between displayed front
        or back sides

        Returns:
            flip_button (ipywidgets.Button)
        """
        # build the button widget
        flip_button = ipywidgets.Button(description='Flip Card',
                                        button_style='success')
        # assign callback
        flip_button.on_click(self.__card_flip_callback)
        # save the widget 
        self.__widgets['card_flip_btn'] = flip_button
        return flip_button

    def __card_flip_callback(self, btn):
        """
        Callback function to be triggered
        when the flip_button is clicked.
        This will swap the text displayed
        on the card between the front text
        and the back text.

        Parameters:
            btn (ipywidgets.Button): this is the button object
                                     that was clicked
        """
        # figure out which side of the
        # card to display now
        if self.__displayed_side == 'Front':
            new_card_widget_to_show = self.__widgets['card_back']
            new_card_side = 'Back'
        else:
            new_card_widget_to_show = self.__widgets['card_front']
            new_card_side = 'Front'

        # update the child of the card_face box 
        self.__widgets['card_face'].children = [new_card_widget_to_show]

        # update the card_side widget with the side
        # that is now being displayed
        self.__set_card_side_text(new_card_side)
        