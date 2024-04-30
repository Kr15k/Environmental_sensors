# writes an HTTP header to the request
async def naw_write_http_header(request, content_type='text/html'):
    """
    HTTP Header
    Content types:
    json: application/json
    """
    request.write("HTTP/1.1 200 OK\r\n")
    request.write("Content-Type: {}\r\n\r\n".format(content_type))
    #request.write('Connection: close\r\n\r\n')

# renders a template string by replacing placeholders with provided values
def render_template_string(s, **kwargs):
    h = s
    for k, v in kwargs.items():
        h = h.replace('{{ ' + str(k) + ' }}', v)
    return h

# reads a template file and renders it with provided values
def render_template(template, **kwargs):
    f = open('/templates/'+template)
    s = f.read()
    return render_template_string(s, **kwargs)

# renders template with set values
def test():
    s = render_template('index.html',
            temperature_bmp='99.99',
            pressure='9999',
            tVOC='2',
            eCO2='402',
            temperature_hdc='99',
            humidity='43',
        )
    #print(s)

# runs if called from main
if __name__ == '__main__':
    test()
