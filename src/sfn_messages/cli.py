import json
import sys
from argparse import ArgumentParser

from sfn_messages.core import get_message_code, load_message_class

parser = ArgumentParser()
subparsers = parser.add_subparsers(dest='action', metavar='action')

to_xml = subparsers.add_parser('toxml', help='Convert JSON to XML')
to_xml.add_argument('-m', '--message-code')
to_xml.add_argument('-i', '--input', default=0, required=False)
to_xml.add_argument('-o', '--output', default=1, required=False)

to_json = subparsers.add_parser('tojson', help='Convert XML to JSON')
to_json.add_argument('-m', '--message-code')
to_json.add_argument('--indent', type=int, default=None)
to_json.add_argument('-i', '--input', default=0, required=False)
to_json.add_argument('-o', '--output', default=1, required=False)


def main() -> None:
    args = parser.parse_args()
    match args.action:
        case 'toxml':
            with open(args.input) as f_input, open(args.output, 'w') as f_output:  # noqa: PTH123
                input_message = json.loads(f_input.read())
                message_code = args.message_code if args.message_code else input_message['message_code']
                message_class = load_message_class(message_code)
                message = message_class.model_validate(input_message)
                print(message.to_xml(), file=f_output)
        case 'tojson':
            with open(args.input) as f_input, open(args.output, 'w') as f_output:  # noqa: PTH123
                input_message = f_input.read()
                message_code = args.message_code if args.message_code else get_message_code(input_message)
                message_class = load_message_class(message_code)
                message = message_class.from_xml(input_message)
                print(message.model_dump_json(indent=args.indent), file=f_output)
        case _:
            parser.print_usage()
            sys.exit(2)


if __name__ == '__main__':
    main()
