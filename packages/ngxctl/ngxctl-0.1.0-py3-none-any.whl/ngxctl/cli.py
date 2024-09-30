# ngxctl/cli.py

import click
from ngxctl.cmds import top
from ngxctl.cmds import extractor
from ngxctl.utils import config_parser  # 假设你有一个配置解析工具


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-c', '--conf', default='/etc/nginx/nginx.conf',
              help='Specify the Nginx configuration file. Default is /etc/nginx/nginx.conf.')
@click.option('--show-vars', is_flag=True,
              help='List all params that are available for access log.')
@click.option('--show-logs', is_flag=True,
              help='List all access log and error log related information.')
# @click.option('--follow/--no-follow', default=True,
#               help='Follow new lines in the log, similar to tail -f command.')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, conf, show_vars, show_logs, debug):
    """ngxctl: A command-line tool for managing and analyzing Nginx."""

    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    # debug 参数, 暂时没啥用
    ctx.obj['DEBUG'] = debug


    # payload 对象
    payload = dict()
    if not os.path.exists(conf):
        raise FileNotFoundError(f"{conf} does not exist")

    if conf.endswith(".json"):
        payload = json.load(open(conf, 'r', encoding="utf-8"))
    else:
        payload = crossplane.parse(conf)

    ctx.obj['payload'] = payload

    # 提取log_path & log format & 放到ctx之中
    log_path_results = config_parser.load_and_extract_log_paths(ngx_cfg_json_dict=payload)
    log_format_results = config_parser.load_and_extract_log_formats(ngx_cfg_json_dict=payload)
    ctx.obj['log_path_results'] = log_path_results
    ctx.obj['log_format_results'] = log_format_results

    if show_vars:
        variables = config_parser.get_log_format_used_fields(log_path_results, log_format_results)
        table_data = [[item] for item in variables]
        print(tabulate.tabulate(table_data, headers=['Variables'], tablefmt='orgtbl'))
        return

    if show_logs:
        table_data = []
        headers = ['server_name', 'file_name', 'log_path']
        for item in log_path_results:
            if item['log_type'] == 'access_log':
                row = []
                for header in headers:
                    if header == 'log_path':
                        row.append(
                            item.get('log_args')[0]
                        )
                    else:
                        row.append(
                            item.get(header, '')
                        )
                table_data.append(row)
        print(tabulate.tabulate(table_data, headers=headers, tablefmt='orgtbl'))
        return


# Add subcommands to the cli group
cli.add_command(top.top)
cli.add_command(extractor.extract)

if __name__ == "__main__":
    cli()