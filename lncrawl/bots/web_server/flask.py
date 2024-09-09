from flask import Flask, request, jsonify
from ...core.app import App
from ...core.crawler import Crawler
from ...core.sources import crawler_list, prepare_crawler, rejected_sources
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok'})

@app.route('/api/supported/', methods=['POST'])
def supported_novels():
    data = request.json

    if not (url := data.get('url')):
        return jsonify({'message': 'mssing url'}), 400
    
    try:
        prepare_crawler(url).__del__()
    except Exception as e:
        return jsonify({'message': str(e)}), 404
    
    return jsonify({'is_supported': True})

@app.route('/api/get/info', methods=['POST'])
def get_novel_info():
    data = request.json

    if not (url := data.get('url')):
        return jsonify({'message': 'mssing url'}), 400
    try:
        crawler = prepare_crawler(url)
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    print(url)
    
    lnc = App()
    lnc.initialize()

    lnc.user_input = url
    lnc.crawler = crawler

    lnc.get_novel_info()

    title = lnc.crawler.novel_title
    author = lnc.crawler.novel_author
    synopsis = lnc.crawler.novel_synopsis
    cover = lnc.crawler.novel_cover
    tags = lnc.crawler.novel_tags
    volumes = lnc.crawler.volumes
    chapters = lnc.crawler.chapters
    summary = lnc.crawler.novel_synopsis

    novel = {
        'title': title,
        'author': author,
        'synopsis': synopsis,
        'cover': cover,
        'tags': tags,
        'volumes': volumes,
        'chapters': chapters,
        'summary': summary
    }

    lnc.destroy()

    return jsonify(novel)

# could possibly pass query params such as start, end.
# default is 0, -1
@app.route('/api/get/chapters', methods=['POST'])
def get_chapters():
    data = request.json

    if not (url := data.get('url')):
        return jsonify({'message': 'mssing url'}), 400
    try:
        crawler = prepare_crawler(url)
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
    lnc = App()
    lnc.initialize()

    lnc.user_input = url
    lnc.crawler = crawler

    lnc.get_novel_info()

    chapters = lnc.crawler.chapters

    inital_chatpers = request.args.get('start', 0)
    final_chapters = request.args.get('end', -1)

    app.crawler.download_chapters(app.chapters[inital_chatpers, final_chapters])

    lnc.destroy()

    return jsonify(chapters)