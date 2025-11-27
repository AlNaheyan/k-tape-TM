#!/usr/bin/env python3

import sys

BLANK = '_'  # underscore is used as blank in spec

class Transition:
    def __init__(self, rule_num, curr_state, input_syms, next_state, write_syms, directions, raw_line):
        self.rule_num = rule_num
        self.curr_state = curr_state
        self.input_syms = input_syms      # list length k
        self.next_state = next_state
        self.write_syms = write_syms      # list length k
        self.directions = directions      # list length k
        self.raw_line = raw_line          # original text of the rule (for echo)


class TuringMachine:
    def __init__(self, name, k, max_tape_len, max_steps,
                 sigma, gammas, states, start_state, accept_state, reject_state,
                 transitions):
        self.name = name
        self.k = k
        self.max_tape_len = max_tape_len
        self.max_steps = max_steps
        self.sigma = sigma              # set of chars for tape 1
        self.gammas = gammas            # list of sets, one per tape
        self.states = states
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.transitions = transitions  # list of Transition (in order)

    def reset_for_problem(self, init_strings):
        """
        init_strings: list of k strings for the tapes
        """
        # Initialize tapes with blanks
        self.tapes = []
        self.heads = []
        for i in range(self.k):
            tape = [BLANK] * self.max_tape_len
            s = init_strings[i]
            for j, ch in enumerate(s):
                if j >= self.max_tape_len:
                    break
                tape[j] = ch
            self.tapes.append(tape)
            self.heads.append(0)  # heads start at position 0

        self.curr_state = self.start_state
        self.step_count = 0

    def current_symbols(self):
        syms = []
        for i in range(self.k):
            pos = self.heads[i]
            if pos < 0 or pos >= self.max_tape_len:
                # outside tape bounds, treat as blank or error
                syms.append(BLANK)
            else:
                syms.append(self.tapes[i][pos])
        return syms

    def find_matching_transition(self, curr_syms):
        """
        curr_syms: list of length k
        returns Transition or None
        """
        for tr in self.transitions:
            if tr.curr_state != self.curr_state:
                continue
            match = True
            for i in range(self.k):
                need = tr.input_syms[i]
                have = curr_syms[i]
                if need == '*':
                    continue
                if need != have:
                    match = False
                    break
            if match:
                return tr
        return None

    def validate_symbols(self, curr_syms):
        """
        Check that the characters under the heads belong to the correct Γ for each tape.
        BLANK is always allowed.
        """
        for i in range(self.k):
            ch = curr_syms[i]
            if ch == BLANK:
                continue
            if ch not in self.gammas[i]:
                return False
        return True

    def run_on_problem(self, init_strings, tape_file_name, problem_index):
        """
        Run TM on one set of k lines. Print trace to stdout as required.
        """
        self.reset_for_problem(init_strings)

        # Print initial tapes
        for i in range(self.k):
            content = ''.join(self.tapes[i]).rstrip(BLANK)
            print(f"Tape {i+1}: {content}")

        # Run transitions
        while True:
            if self.step_count >= self.max_steps:
                # exceeded max steps
                print("Error")  # you can optionally add details
                self.print_final_tapes()
                return

            curr_syms = self.current_symbols()

            # validate symbols
            if not self.validate_symbols(curr_syms):
                print("Error")
                self.print_final_tapes()
                return

            # accept / reject check before consuming a rule?
            if self.curr_state == self.accept_state:
                print("Accepted")
                self.print_final_tapes()
                return
            if self.curr_state == self.reject_state:
                print("Rejected")
                self.print_final_tapes()
                return

            tr = self.find_matching_transition(curr_syms)
            if tr is None:
                # no rule covers this configuration
                print("Error")
                self.print_final_tapes()
                return

            self.step_count += 1

            # Build trace line:
            # Step number, Rule Number{, Tape Index}^k, Initial State Name,
            # {Input Symbol}^k, New State Name, {New Tape Symbol}^k, {Direction}^k
            fields = []
            fields.append(str(self.step_count))
            fields.append(str(tr.rule_num))

            # Tape indices (heads before move)
            for i in range(self.k):
                fields.append(str(self.heads[i]))

            # Initial state
            fields.append(self.curr_state)

            # Input symbols
            for ch in curr_syms:
                fields.append(ch)

            # New state
            fields.append(tr.next_state)

            # New tape symbols
            # (here '*' means "keep old symbol")
            new_syms = []
            for i in range(self.k):
                write_ch = tr.write_syms[i]
                if write_ch == '*':
                    # no change
                    new_syms.append(curr_syms[i])
                else:
                    new_syms.append(write_ch)
            for ch in new_syms:
                fields.append(ch)

            # Directions
            for d in tr.directions:
                fields.append(d)

            print(','.join(fields))

            # Apply changes to machine state
            # 1) write symbols
            for i in range(self.k):
                pos = self.heads[i]
                if 0 <= pos < self.max_tape_len:
                    self.tapes[i][pos] = new_syms[i]
                else:
                    # step outside bounds, treat as error
                    print("Error")
                    self.print_final_tapes()
                    return

            # 2) move heads
            for i in range(self.k):
                d = tr.directions[i]
                if d == 'L':
                    self.heads[i] -= 1
                elif d == 'R':
                    self.heads[i] += 1
                elif d == 'S':
                    pass
                else:
                    print("Error")
                    self.print_final_tapes()
                    return

                if self.heads[i] < 0 or self.heads[i] >= self.max_tape_len:
                    print("Error")
                    self.print_final_tapes()
                    return

            # 3) change state
            self.curr_state = tr.next_state

            # Accept / reject after applying
            if self.curr_state == self.accept_state:
                print("Accepted")
                self.print_final_tapes()
                return
            if self.curr_state == self.reject_state:
                print("Rejected")
                self.print_final_tapes()
                return

    def print_final_tapes(self):
        for i in range(self.k):
            content = ''.join(self.tapes[i]).rstrip(BLANK)
            print(f"Tape {i+1}: {content}")


def parse_machine_file(path):
    with open(path, 'r') as f:
        lines = [line.rstrip('\n').rstrip('\r') for line in f]

    if len(lines) < 6:
        raise ValueError("Machine file too short")

    # Line 1: name, k, max_tape_len, max_steps
    parts = [p.strip() for p in lines[0].split(',') if p.strip() != '']
    name = parts[0]
    k = int(parts[1])
    max_tape_len = int(parts[2])
    max_steps = int(parts[3])

    # Line 2: sigma alphabet (tape 1)
    sigma_parts = [p.strip() for p in lines[1].split(',') if p.strip() != '']
    sigma = set(sigma_parts)

    # Line 3: states
    states = [p.strip() for p in lines[2].split(',') if p.strip() != '']

    # Line 4: start state
    start_state = lines[3].strip()

    # Line 5: accept, reject
    acc_rej_parts = [p.strip() for p in lines[4].split(',') if p.strip() != '']
    accept_state = acc_rej_parts[0]
    reject_state = acc_rej_parts[1]

    # Next k lines: gamma for each tape
    gammas = []
    for i in range(k):
        gamma_parts = [p.strip() for p in lines[5 + i].split(',') if p.strip() != '']
        gamma_set = set(gamma_parts)
        # BLANK is automatically included
        gamma_set.add(BLANK)
        gammas.append(gamma_set)

    transitions = []
    rule_start_line = 5 + k
    rule_num = 1

    for line in lines[rule_start_line:]:
        line = line.strip()
        if line == '':
            continue
        # optionally ignore comments
        if line.startswith('#'):
            continue

        parts = [p.strip() for p in line.split(',')]
        expected_len = 2 + 3 * k  # 1 curr_state + k input + 1 next_state + k write + k dir
        if len(parts) != expected_len:
            raise ValueError(f"Bad rule line (wrong number of fields): {line}")

        idx = 0
        curr_state = parts[idx]; idx += 1
        input_syms = parts[idx:idx + k]; idx += k
        next_state = parts[idx]; idx += 1
        write_syms = parts[idx:idx + k]; idx += k
        directions = parts[idx:idx + k]; idx += k

        tr = Transition(rule_num, curr_state, input_syms, next_state, write_syms, directions, line)
        transitions.append(tr)

        # Echo rule as we read it
        print(f"{rule_num}:{line}")
        rule_num += 1

    tm = TuringMachine(name, k, max_tape_len, max_steps,
                       sigma, gammas, states, start_state,
                       accept_state, reject_state, transitions)
    return tm


def run_tape_file(tm, tape_file_path):
    print(f"Tape file: {tape_file_path}")
    with open(tape_file_path, 'r') as f:
        all_lines = [line.rstrip('\n').rstrip('\r') for line in f]

    i = 0
    problem_idx = 0
    n = len(all_lines)
    while i < n:
        # Read k lines per problem
        init_strings = []
        for t in range(tm.k):
            if i >= n:
                init_strings = None
                break
            init_strings.append(all_lines[i])
            i += 1

        if not init_strings or len(init_strings) < tm.k:
            break  # no more full problems

        problem_idx += 1
        tm.run_on_problem(init_strings, tape_file_path, problem_idx)


def main():
    if len(sys.argv) != 3:
        print("Usage: python tm_netid.py <machine_file> <tape_file>")
        sys.exit(1)

    machine_file = sys.argv[1]
    tape_file = sys.argv[2]

    tm = parse_machine_file(machine_file)
    run_tape_file(tm, tape_file)


if __name__ == "__main__":
    main()