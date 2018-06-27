import os
import re
import sys
import urllib.parse

DATA_DIR = os.getenv('DATA_DIR', './data')


def main(ctx, res_file, meta_file):
    # parse response
    response = None
    with open(res_file, 'rb') as f:
        response = f.read()
        f.close()
    params = urllib.parse.parse_qs(response.decode('utf-8'))

    # save the authentication response parametes/fields in separate files
    for par in ['SAMLResponse', 'RelayState', 'Signature', 'SigAlg']:
        if par in params:
            content = re.sub(r'[\s]', '', params[par][0])
        else:
            content = ''

        fname = '%s/%s.%s.response.txt' % (DATA_DIR, par, ctx)
        with open(fname, 'w') as f:
            f.write(content)
            f.close()

    '''
    # if HTTP-Redirect extract the signing certificate(s) from the metadata
    if ('Signature' in params) and ('SigAlg' in params):
        # load metadata file
        with open(meta_file, 'rb') as f:
            meta = f.read()
            f.close()
        doc = ET.parse(BytesIO(meta))

        # remove the namespace to simplify XPath
        root = doc.getroot()
        for elem in root.getiterator():
            if not hasattr(elem.tag, 'find'):
                continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i+1:]
        lxml.objectify.deannotate(root, cleanup_namespaces=True)

        # save each certificate in a specific file (*.signature.pem)
        certs = doc.xpath('//SPSSODescriptor/KeyDescriptor[@use="signing"]'
                          '/KeyInfo/X509Data/X509Certificate')
        for cert in certs:
            common.dump_pem.dump_response_pem(cert, ctx, 'signature', DATA_DIR)
    '''

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0)
