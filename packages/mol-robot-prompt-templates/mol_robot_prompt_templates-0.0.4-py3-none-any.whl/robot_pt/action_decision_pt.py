import textwrap

from .state_description_pt import state_description_pt


def action_decision_pt(state_chunks: str) -> str:
    '''
    Prompt for Action Decision LLM that predicts the optimal action token.

    Args:
        state_chunks: Sequence of state information chunks formatted as follows:
            ---
            topic: /asr
            ts: 2024-08-31 17:45:23
            data: <Robot heard voice> User says: Hey robot, I'm heading out for the day.
            ---
            topic: /action_response
            ts: 2024-08-31 17:45:25
            data: <Robot completed reply action> Robot says: Certainly! I hope you had a productive day. Is there anything you need help with before you leave?
            ---
            topic: /asr
            ts: 2024-08-31 17:45:32
            data: <Robot heard voice> User says: No, I think I'm all set. Just wanted to say goodbye.
            ---
            topic: /action_response
            ts: 2024-08-31 17:45:34
            data: <Robot completed reply action> Robot says: That's very kind of you, sweetie. Have a wonderful evening and a safe trip home!
            ---

    Returns:

    '''
    state_template = textwrap.dedent('''
        <state_header>
        {}
        </state_header>

        <retrieved_memory>
        </retrieved_memory>

        <state_chunks>
        {}
        </state_chunks>
    ''')

    instruction_template = textwrap.dedent('''
        Output the optimal action the robot should take in order to achieve the goal based on the following robot world state:
        {}
        The robot outputs what action to take to optimally help the user and follow user instructions. The robot should provide information and assistance as needed. Generally the robot pursues conversation with the user but remains quiet unless user is speaking with the robot.

        Output the single character (a or b) of the optimal valid action the robot should take among the following list of valid actions. Do not explain the reason for choosing the action's character. Only output the action's character.

        List of valid actions:
        a: <Robot idle action> Robot decides to take no new action
        b: <Robot reply action> Robot decides to reply to user
    ''')

    state_descr = state_description_pt()

    state = state_template.format(state_descr, state_chunks)
    prompt = instruction_template.format(state)

    # Remove leading/trailing line breaks
    prompt = prompt.strip()

    return prompt


if __name__ == '__main__':

    state_chunks = textwrap.dedent('''
        ---
        topic: /asr
        ts: 2024-08-31 17:45:23
        data: <Robot heard voice> User says: Hey robot, I'm heading out for the day.
        ---
        topic: /action_response
        ts: 2024-08-31 17:45:25
        data: <Robot completed reply action> Robot says: Certainly! I hope you had a productive day. Is there anything you need help with before you leave?
        ---
        topic: /asr
        ts: 2024-08-31 17:45:32
        data: <Robot heard voice> User says: No, I think I'm all set. Just wanted to say goodbye.
        ---
        topic: /action_response
        ts: 2024-08-31 17:45:34
        data: <Robot completed reply action> Robot says: That's very kind of you, sweetie. Have a wonderful evening and a safe trip home!
        ---
    ''')

    state_chunks = state_chunks.strip()

    # Remove leading/trailing line breaks
    prompt = action_decision_pt(state_chunks)

    print(prompt)
