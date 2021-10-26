from bs4 import BeautifulSoup as bs
from requests import request
import re
from disnake import Embed
import lxml


CORE_INDEX = 'https://raw.githubusercontent.com/aurorabuilder/elements/master/core.index'


class Lookup:

    def __init__(self, search):
        self.search_str = search
        self.indexes = []
        self.__lookup_post__()

    def __lookup_post__(self):
        _r = request('GET', CORE_INDEX)
        _bs = bs(_r.text, 'lxml')
        _indexes = _bs.files.find_all(url=re.compile('index'))
        self.indexes = [_i['url'] for _i in _indexes]

    @property
    def lang_urls(self):
        # for each index
        sources_index = []
        for index in self.indexes:
            _r = request('GET', index)
            _bs = bs(_r.text, 'lxml')
            _lang = _bs.find(attrs={"name": re.compile("languages", re.I)})
            sources_index.append(_lang['url']) if _lang else 0
        return sources_index

    @property
    def feat_urls(self):
        # for each index
        sources_index = []
        for index in self.indexes:
            _r = request('GET', index)
            _bs = bs(_r.text, 'lxml')
            _feat = _bs.find(attrs={"name": re.compile("feats", re.I)})
            sources_index.append(_feat['url']) if _feat else 0
        return sources_index


class LookupLanguage(Lookup):

    def __init__(self, search):
        super().__init__(search)
        self.results = []
        self.name = ""
        self.standard = ""
        self.speakers = ""
        self.script = ""
        self.source = ""
        self.match_found = False

        self.__post__()

    def __post__(self):
        _rl = ''
        for url in self.lang_urls:
            _r = request('GET', url)
            _rl += _r.text
        _bs = bs(_rl, 'lxml')
        _e: list = _bs.findAll(attrs={"name": re.compile(self.search_str, re.I), "type": "Language"})
        # check to see if any of the finds is an exact match, by iterating
        for lang in _e:
            if len(self.search_str) == len(lang['name']) and self.search_str.title() == lang['name']:
                # self.results = [lang['name']]
                self.match_found = True
                self.compile_results(lang)
                break
        # check to see if if there are only one result
        if len(_e) != 1 and not self.match_found:
            self.results = [(_i['name'], _i['source']) for _i in _e]
        else:
            self.compile_results(_e[0])

    def compile_results(self, lang):
        _script = lang.setters.find(attrs={"name": "script"})
        self.results = [lang['name']]
        self.name = lang['name']
        self.standard = lang.supports.string
        self.speakers = lang.setters.find(attrs={"name": "speakers"}).string
        self.script = _script.string if _script else "None"
        self.source = lang['source']

    def build_embed(self, ctx):
        _e = Embed(title="Language Lookup",
                   description=f"Searching for keyword: `{self.search_str}`",
                   type='rich')
        _e.set_footer(text=f'{ctx.author.name}')
        _e.set_thumbnail(ctx.author.display_avatar.url)
        _r = f'```css\n'
        if len(self.results) != 1:
            for lang, source in self.results:
                _r += f'{lang}.{source.replace(" ", "_").replace("’", "")}\n'
        else:
            _r += f'Name: "{self.name}"\n'
            _r += f'Standard: "{self.standard}"\n'
            _r += f'Speakers: "{self.speakers}"\n'
            _r += f'Script: "{self.script}"\n'
            _r += f'Source: "{self.source}"\n'
        _r += f'```'
        _e.add_field(name="Results", value=_r)
        return _e


class LookupFeat(Lookup):

    def __init__(self, search):
        super().__init__(search)
        self.results = []
        self.name = ""
        self.description = ""
        self.sheet = ""
        self.rules = ""
        self.source = ""
        self.match_found = False
        self.__post__()

    def __post__(self):
        _rl = ''
        for url in self.feat_urls:
            _r = request('GET', url)
            _rl += _r.text
        _bs = bs(_rl, 'lxml')
        _e: list = _bs.findAll(attrs={"name": re.compile(self.search_str, re.I), "type": "Feat"})
        # check to see if any of the finds is an exact match, by iterating
        for feat in _e:
            if len(self.search_str) == len(feat['name']) and self.search_str.title() == feat['name']:
                # self.results = [lang['name']]
                self.match_found = True
                self.compile_results(feat)
                break
        # check to see if if there are only one result
        if len(_e) != 1 and not self.match_found:
            self.results = [(_i['name'], _i['source']) for _i in _e]
        else:
            self.compile_results(_e[0])

    def compile_results(self, feat):

        self.results = [feat['name']]
        self.name = feat['name']
        self.description = feat.description.text
        self.sheet = feat.sheet.description.text
        self.rules = f'{feat.rules.stat["name"].title()} +{feat.rules.stat["value"]}'
        self.source = feat['source']

    def build_embed(self, ctx):
        _e = Embed(title="Feat Lookup",
                   description=f"Searching for keyword: `{self.search_str}`",
                   type='rich')
        _e.set_footer(text=f'{ctx.author.name}')
        _e.set_thumbnail(ctx.author.display_avatar.url)
        _r = f'```css\n'
        if len(self.results) != 1:
            for feat, source in self.results:
                _r += f'{feat}.{source.replace(" ", "_").replace("’", "")}\n'
        else:
            _r += f'Name: "{self.name}"\n'
            _r += f'Description: "{self.description}"\n'
            _r += f'Sheet Actions: "{self.sheet}"\n'
            _r += f'Rules: "{self.rules}"\n'
            _r += f'Source: "{self.source}"\n'
        _r += f'```'
        _e.add_field(name="Results", value=_r)
        return _e
