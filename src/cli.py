import click
import auth
import features
import logging
import sys

LOGGING_LEVEL = [
    logging.INFO,
    logging.WARNING,
    logging.DEBUG
]

@click.command()
@click.option('--email', '-e', help='facebook email', required=False)
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
              type=click.Choice(['complete', 'simple', 'facebook']),
              default='complete',
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
        click.echo('you provide your own token, if it doesn\t work try with your facebook email password')

    if email and password:
        token = auth.login(email, password)
        click.echo('create a fresh token with facebook email address and password')

    if token:
        auth.write_token(token)
        click.echo('generate a token: {} and save it to: {}'.format(token, 'conf/token.txt'))

    try:
        recomendations_raw = features.recommendations()
    except:
        click.echo('your token has probably expired, you need to provide your creditentials either by your facebook account and password or with your own token, if don\t trust the code source the application does nothing with your facebook account and password, expect a call to the happn api to get a token')
        click.echo('python3 cli.py --email example@gmail.com --password password')
        sys.exit()

    if download:
        download_path = download_path or features.IMAGE_FOLDER
        features.download_image(recomendations_raw)

    recommendations_output = ''
    if view == 'complete':
        recommendations_output = recomendations_raw
    elif view == 'simple':
        recommendations_output = features.view_simple(recomendations_raw)
    elif view == 'facebook':
        recommendations_output = features.facebook_view(recommendations_output)
    else:
        recommendations_output = recomendations_raw

    if save_path:
        features.save_minettes(recommendations_output, save_path)

    click.echo(recommendations_output)



if __name__ == '__main__':
    main()
