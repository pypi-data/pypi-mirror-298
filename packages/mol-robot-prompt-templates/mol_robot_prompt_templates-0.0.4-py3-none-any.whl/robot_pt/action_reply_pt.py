import textwrap

from .state_description_pt import state_description_pt


def action_reply_pt(state_chunks: str) -> str:
    '''
    Prompt for Action Reply LLM to generate a reply based on the current robot
    state.

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
        Text prompt for the Action Reply LLM.
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
        Generate a vocal reply for the robot to fullfill the user's request or answer the user's question based on contextual information in the robot world state:
        {}
        You are the robot.
        Reply to the user in a brief, concise, and affectionate conversational manner.
        Reply only in a single sentence if possible. Reply with multiple sentences only if required to adequately reply to complicated requests or questions.
        Never repeat a previous reply. Expand on the previous reply instead of repeating it.
        Base the reply only on information relevant to the request or question. Ignore unrelated, incoherent, and nonsensical information which might be noise.
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
    prompt = action_reply_pt(state_chunks)

    print(prompt)
