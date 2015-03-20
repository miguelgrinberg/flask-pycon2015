class GuessError(RuntimeError):
    """Custom exception for game errors."""
    pass


class Guess:
    def __init__(self, initial_guess):
        self.data = [{'guess': initial_guess}]

    def expand(self, old_guess, new_guess, question, answer_for_new):
        """Add a new guess to the game.

        Parameters:
            old_guess (str): The existing guess that is being expanded.
            new_guess (str): The new guess added to the game.
            question (str): A question to separate old_guess from new_guess.
            answer_for_new (bool): The answer to the question for new_guess.

        Raises:
            GuessError: Input is invalid.

        Returns:
            None

        Example:
            The example below sets up a "Guess the Programming Language" game
            with Python, C++, Java and Ruby:

                game = Guess('Python')
                game.expand('Python', 'C++', 'Is it interpreted?', True)
                game.expand('C++', 'Java', 'Does it run on a VM?', True)
                game.expand('Python', 'Ruby', 'Does it enforce indentation?',
                            False)
        """
        old_guess_id = self._get_guess_id(old_guess)
        if old_guess_id is None:
            raise GuessError(old_guess + ' is unknown.')
        if self._get_guess_id(new_guess) is not None:
            raise GuessError(new_guess + ' is known already.')
        last_index = len(self.data)
        if answer_for_new:
            self.data.append({'guess': new_guess})
            self.data.append({'guess': old_guess})
        else:
            self.data.append({'guess': old_guess})
            self.data.append({'guess': new_guess})
        self.data[old_guess_id] = {'question': question, 'yes': last_index,
                                   'no': last_index + 1}

    def get_question(self, id=0):
        """Get the current question for this game.

        Parameters:
            id (int): The identifier of the current position in the game.

        Returns:
            The question for the given position in the game if available, or
            None otherwise. If None is returned, that means that the game has
            reached a point where a guess is available.

        Raises:
            IndexError: Unknown id.
        """
        return self.data[id].get('question')

    def get_guess(self, id=0):
        """Get the guess for this game.

        Parameters:
            id (int): The identifier of the current position in the game.

        Returns:
            The guess for the given position in the game if available, or None
            otherwise. If None is returned, that means there are still
            questions that need to be answered.

        Raises:
            IndexError: Unknown id.
        """
        return self.data[id].get('guess')

    def answer_question(self, answer, id=0):
        """Provide an answer for the current question.

        Parameters:
            id (int): The identifier of the current position in the game.

        Returns:
            The id for the next position in the game.

        Raises:
            GuessError: The id given does not point to a question.
            IndexError: Unknown id.
        """
        if answer:
            new_id = self.data[id].get('yes')
        else:
            new_id = self.data[id].get('no')
        if new_id is None:
            raise GuessError('Not a question')
        return new_id

    def _get_guess_id(self, guess):
        for i in range(len(self.data)):
            if self.data[i].get('guess') == guess:
                return i
        return None
