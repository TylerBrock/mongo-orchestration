# coding=utf-8
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import json
import sys

sys.path.insert(0, '..')
from lib.rs import RS
from bottle import route, request, response, abort, run


def send_result(code, result=None):
    logger.debug("send_result({code}, {result})".format(**locals()))
    content = None
    response.content_type = None
    if result is not None:
            content = json.dumps(result)
            response.content_type = "application/json"
    response.status = code
    if code > 399:
        return abort(code, content)
    return content


@route('/rs', method='POST')
def rs_create():
    logger.debug("rs_create()")
    data = {}
    json_data = request.body.read()
    if json_data:
        data = json.loads(json_data)
    try:
        rs_id = RS().rs_new(data)
        result = RS().repl_info(rs_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_create".format(**locals()))
        return send_result(500)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs', method='GET')
def rs_list():
    logger.debug("rs_list()")
    try:
        data = [info for info in RS()]
    except StandardError as e:
        logger.error("Exception {e} while rs_list".format(**locals()))
        return send_result(500)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, data)


@route('/rs/<rs_id>', method='GET')
def rs_info(rs_id):
    logger.debug("rs_info({rs_id})".format(**locals()))
    if rs_id not in RS():
        return send_result(404)
    try:
        result = RS().repl_info(rs_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_info".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>', method='DELETE')
def rs_del(rs_id):
    logger.debug("rs_del({rs_id})".format(**locals()))
    if rs_id not in RS():
        return send_result(404)
    try:
        result = RS().rs_del(rs_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_del".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(204, result)


@route('/rs/<rs_id>/members', method='POST')
def rs_member_add(rs_id):
    logger.debug("rs_member_add({rs_id})".format(**locals()))
    if rs_id not in RS():
        return send_result(404)
    data = {}
    json_data = request.body.read()
    if json_data:
        data = json.loads(json_data)
    try:
        member_id = RS().rs_member_add(rs_id, data)
        result = RS().rs_member_info(rs_id, member_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_member_add".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>/members', method='GET')
def rs_members(rs_id):
    logger.debug("rs_members({rs_id})".format(**locals()))
    if rs_id not in RS():
        return send_result(404)
    try:
        result = RS().rs_members(rs_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_members".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>/secondaries', method='GET')
def rs_secondaries(rs_id):
    logger.debug("rs_secondaries({rs_id})".format(**locals()))
    if rs_id not in RS():
        return send_result(404)
    try:
        result = RS().rs_secondaries(rs_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_secondaries".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>/arbiters', method='GET')
def rs_arbiters(rs_id):
    logger.debug("rs_arbiters({rs_id})".format(**locals()))
    if rs_id not in RS():
        return send_result(404)
    try:
        result = RS().rs_arbiters(rs_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_arbiters".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>/hidden', method='GET')
def rs_hidden(rs_id):
    logger.debug("rs_hidden({rs_id})".format(**locals()))
    if rs_id not in RS():
        return send_result(404)
    try:
        result = RS().rs_hidden(rs_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_hidden".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>/members/<member_id>', method='GET')
def rs_member_info(rs_id, member_id):
    logger.debug("rs_member_info({rs_id}, {member_id})".format(**locals()))
    member_id = int(member_id)
    if rs_id not in RS():
        return send_result(404)
    try:
        result = RS().rs_member_info(rs_id, member_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_member_info".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>/members/<member_id>', method='DELETE')
def rs_member_del(rs_id, member_id):
    logger.debug("rs_member_del({rs_id}), {member_id}".format(**locals()))
    member_id = int(member_id)
    if rs_id not in RS():
        return send_result(404)
    try:
        result = RS().rs_member_del(rs_id, member_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_member_del".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>/members/<member_id>', method='PUT')
def rs_member_update(rs_id, member_id):
    logger.debug("rs_member_update({rs_id}, {member_id})".format(**locals()))
    member_id = int(member_id)
    if rs_id not in RS():
        return send_result(404)
    data = {}
    json_data = request.body.read()
    if json_data:
        data = json.loads(json_data)
    try:
        RS().rs_member_update(rs_id, member_id, data)
        result = RS().rs_member_info(rs_id, member_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_member_update".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>/members/<member_id>/<command:re:(start)|(stop)|(restart)>', method='PUT')
def rs_member_command(rs_id, member_id, command):
    logger.debug("rs_member_command({rs_id}, {member_id}, {command})".format(**locals()))
    member_id = int(member_id)
    if rs_id not in RS():
        return send_result(404)
    try:
        result = RS().rs_member_command(rs_id, member_id, command)
        if result:
            return send_result(200)
        return send_result(400)
    except StandardError as e:
        logger.error("Exception {e} while rs_member_command".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)


@route('/rs/<rs_id>/primary', method='GET')
def rs_member_primary(rs_id):
    logger.debug("rs_member_primary({rs_id})".format(**locals()))
    if rs_id not in RS():
        return send_result(404)

    try:
        result = RS().rs_primary(rs_id)
    except StandardError as e:
        logger.error("Exception {e} while rs_member_primary".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200, result)


@route('/rs/<rs_id>/primary/stepdown', method='PUT')
def rs_primary_stepdown(rs_id):
    logger.debug("rs_primary_stepdown({rs_id})".format(**locals()))
    if rs_id not in RS():
        return send_result(404)

    data = {}
    json_data = request.body.read()
    if json_data:
        data = json.loads(json_data)
    try:
        RS().rs_primary_stepdown(rs_id, data.get('timeout', 60))
    except StandardError as e:
        logger.error("Exception {e} while rs_primary_stepdown".format(**locals()))
        return send_result(400)
    except Exception as e:
        logger.critical("Unknown Exception {e}".format(**locals()))
        return send_result(500)
    return send_result(200)


if __name__ == '__main__':
    rs = RS()
    rs.set_settings('/tmp/mongo-orchestration.rs-storage', '')
    run(host='localhost', port=8889, debug=True, reloader=False)