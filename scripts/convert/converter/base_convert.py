import os
import yaml


class BaseConverter(object):
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self._parase_modelfile()

    def _parase_modelfile(self):
        with open(os.path.join(self.input_dir, 'ormbfile.yaml'), 'r') as f:
            data = yaml.load(f)

        self.author = data.get('author', None)
        self.input_value = data['signature']['inputs']
        self.output_value = data['signature']['outputs']

    def _write_output_ormbfile(self):
        output_ormbfile = dict()
        if self.author:
            output_ormbfile['author'] = self.author

        output_ormbfile['format'] = os.environ['FORMAT']
        output_ormbfile['signature'] = {}
        output_ormbfile['signature']['inputs'] = self.input_value
        output_ormbfile['signature']['outputs'] = self.output_value

        with open(os.path.join(self.output_dir, 'ormbfile.yaml'), 'w') as f:
            yaml.dump(output_ormbfile, f)

    def _find_with_extension(self, extension):
        dir = os.path.join(self.input_dir, 'model')
        filelist = list(
            filter(lambda f: f.endswith(extension) and not f.startswith('.'),
                   os.listdir(dir)))
        assert (len(filelist) == 1), 'expected one %s file,but found %s' % (
            extension, len(filelist))
        return os.path.join(dir, filelist[0])

    def _find_with_name(self, name):
        dir = os.path.join(self.input_dir, 'model')
        filelist = list(filter(lambda f: f == name, os.listdir(dir)))
        assert (len(filelist) == 1
                ), 'expected one %s file,but found %s' % (name, len(filelist))
        return os.path.join(dir, filelist[0])

    def _convert(self):
        raise NotImplementedError

    def _load_model(self):
        raise NotImplementedError

    def convert(self):
        self._load_model()
        self._convert()
        self._write_output_ormbfile()
