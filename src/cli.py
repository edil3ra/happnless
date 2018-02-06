import click
import auth
import logging
import sys
import os
import json


conf_path = os.path.join(os.path.dirname(__file__), '..', 'conf', 'config.yaml')
token_path = os.path.join(os.path.dirname(__file__), '..', 'conf', 'token.txt')

LOGGING_LEVEL = [
    logging.INFO,
    logging.WARNING,
    logging.DEBUG
]

@click.command()
@click.option('--email', '-m', help='facebook email', required=False)
@click.option('--password', '-p',
              help='password of your facebook account',
              required=False)
@click.option('--token', '-t',
              help='password of your facebook account',
              required=False)
@click.option('--download', '-d',
              help='download images from your recommendations',
              required=False)
@click.option('--download-path',
              help='pathname to store the images',
              required=False)
@click.option('--save-path',
              help='pathname to save your recommendations list',
              required=False)
@click.option('--view', '-l',
              type=click.Choice(['default', 'complete', 'simple', 'facebook']),
              default='default',
              help='get a list of you recommendations')
@click.option('--verbose', '-v', count=True, default=0)
def main(email,
         password,
         token,
         download,
         download_path,
         save_path,
         view,
         verbose):

    if 1 <= verbose <= 3:
        logging.basicConfig(level=verbose - 1)
    else:
        logging.disable = True

    if token:
        click.echo('''
        you provide your own token, if it doesn\t
        work try with your facebook email password
        ''')

    if email and password:
        token = auth.login(email, password)
        click.echo('''
        create a fresh token with
        facebook email address and password
        ''')

    if token:
        auth.write_token(token)
        click.echo('generate a token: {} and save it to: {}'.format(token, 'conf/token.txt'))

    if not os.path.exists(token_path):
        click.echo('You never created a token, create a token first please, see readme')
        sys.exit()

    # make sure it's import after the new token was setted
    import features

    try:
        recomendations_raw = features.recommendations()
    except:
        click.echo('''
        Your token has probably expired\n
        You need to provide your creditentials either by your facebook account
        and password or with your own token)
        Ex: click.echo('python3 cli.py --email example@gmail.com
        --password password
        ''')
        sys.exit()

    if download:
        download_path = download_path or features.IMAGE_FOLDER
        features.download_image(recomendations_raw)

    recommendations_output = ''
    if view == 'complete':
        recommendations_output = json.dumps(recomendations_raw, indent=4)
    elif view == 'simple':
        recommendations_output = json.dumps(
            features.view_simple(recomendations_raw),
            indent=4
        )
    elif view == 'facebook':
        recommendations_output = json.dumps(
            features.view_facebook(recomendations_raw),
            indent=4
        )
    else:
        recommendations_output = len(recomendations_raw)

    if save_path:
        features.save_minettes(recommendations_output, save_path)

    click.echo(recommendations_output)


if __name__ == '__main__':
    main()
