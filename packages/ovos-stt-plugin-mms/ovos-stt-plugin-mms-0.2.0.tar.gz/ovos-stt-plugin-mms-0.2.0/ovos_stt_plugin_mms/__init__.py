from typing import Optional

from ovos_plugin_manager.templates.stt import STT
from ovos_stt_plugin_wav2vec import Wav2VecSTT
from speech_recognition import AudioData
from ovos_utils.lang import standardize_lang_tag


class MMSSTT(STT):
    """see https://huggingface.co/docs/transformers/main/en/model_doc/mms

    @article{pratap2023mms,
          title={Scaling Speech Technology to 1,000+ Languages},
          author={Vineel Pratap and Andros Tjandra and Bowen Shi and Paden Tomasello and Arun Babu and Sayani Kundu
                  and Ali Elkahky and Zhaoheng Ni and Apoorv Vyas and Maryam Fazel-Zarandi and Alexei Baevski and
                  Yossi Adi and Xiaohui Zhang and Wei-Ning Hsu and Alexis Conneau and Michael Auli},
          journal={arXiv},
          year={2023}
    }
    """
    MODELS = ["facebook/mms-1b-all", "facebook/mms-1b-l1107", "facebook/mms-1b-fl102"]
    _LANGS1 = ['afr', 'amh', 'ara', 'asm', 'ast', 'azj-script_latin', 'bel', 'ben', 'bos', 'bul', 'cat', 'ceb', 'ces',
               'ckb', 'cmn-script_simplified', 'cym', 'dan', 'deu', 'ell', 'eng', 'est', 'fas', 'fin', 'fra', 'ful',
               'gle', 'glg', 'guj', 'hau', 'heb', 'hin', 'hrv', 'hun', 'hye', 'ibo', 'ind', 'isl', 'ita', 'jav', 'jpn',
               'kam', 'kan', 'kat', 'kaz', 'kea', 'khm', 'kir', 'kor', 'lao', 'lav', 'lin', 'lit', 'ltz', 'lug', 'luo',
               'mal', 'mar', 'mkd', 'mlt', 'mon', 'mri', 'mya', 'nld', 'nob', 'npi', 'nso', 'nya', 'oci', 'orm', 'ory',
               'pan', 'pol', 'por', 'pus', 'ron', 'rus', 'slk', 'slv', 'sna', 'snd', 'som', 'spa', 'srp-script_latin',
               'swe', 'swh', 'tam', 'tel', 'tgk', 'tgl', 'tha', 'tur', 'ukr', 'umb', 'urd-script_arabic',
               'uzb-script_latin', 'vie', 'wol', 'xho', 'yor', 'yue-script_traditional', 'zlm', 'zul']
    _LANGS2 = _LANGS1 + ['abi', 'abp', 'aca', 'acd', 'ace', 'acf', 'ach', 'acn', 'acr', 'acu', 'ade', 'adh', 'adj',
                         'adx', 'aeu', 'agd', 'agg', 'agn', 'agr', 'agu', 'agx', 'aha', 'ahk', 'aia', 'aka', 'akb',
                         'ake', 'akp', 'alj', 'alp', 'alt', 'alz', 'ame', 'amf', 'ami', 'amk', 'ann', 'any', 'aoz',
                         'apb', 'apr', 'arl', 'asa', 'asg', 'ata', 'atb', 'atg', 'ati', 'atq', 'ava', 'avn', 'avu',
                         'awa', 'awb', 'ayo', 'ayr', 'ayz', 'azb', 'azg', 'azj-script_cyrillic', 'azz', 'bak', 'bam',
                         'ban', 'bao', 'bav', 'bba', 'bbb', 'bbc', 'bbo', 'bcc-script_arabic', 'bcc-script_latin',
                         'bcl', 'bcw', 'bdg', 'bdh', 'bdq', 'bdu', 'bdv', 'beh', 'bem', 'bep', 'bex', 'bfa', 'bfo',
                         'bfy', 'bfz', 'bgc', 'bgq', 'bgr', 'bgt', 'bgw', 'bha', 'bht', 'bhz', 'bib', 'bim', 'bis',
                         'biv', 'bjr', 'bjv', 'bjw', 'bjz', 'bkd', 'bkv', 'blh', 'blt', 'blx', 'blz', 'bmq', 'bmr',
                         'bmu', 'bmv', 'bng', 'bno', 'bnp', 'boa', 'bod', 'boj', 'bom', 'bor', 'bov', 'box', 'bpr',
                         'bps', 'bqc', 'bqi', 'bqj', 'bqp', 'bru', 'bsc', 'bsq', 'bss', 'btd', 'bts', 'btt', 'btx',
                         'bud', 'bus', 'bvc', 'bvz', 'bwq', 'bwu', 'byr', 'bzh', 'bzi', 'bzj', 'caa', 'cab',
                         'cac-dialect_sanmateoixtatan', 'cac-dialect_sansebastiancoatan', 'cak-dialect_central',
                         'cak-dialect_santamariadejesus', 'cak-dialect_santodomingoxenacoj', 'cak-dialect_southcentral',
                         'cak-dialect_western', 'cak-dialect_yepocapa', 'cap', 'car', 'cas', 'cax', 'cbc', 'cbi', 'cbr',
                         'cbs', 'cbt', 'cbu', 'cbv', 'cce', 'cco', 'cdj', 'ceg', 'cek', 'cfm', 'cgc', 'chf', 'chv',
                         'chz', 'cjo', 'cjp', 'cjs', 'cko', 'ckt', 'cla', 'cle', 'cly', 'cme', 'cmo-script_khmer',
                         'cmo-script_latin', 'cmr', 'cnh', 'cni', 'cnl', 'cnt', 'coe', 'cof', 'cok', 'con', 'cot',
                         'cou', 'cpa', 'cpb', 'cpu', 'crh', 'crk-script_latin', 'crk-script_syllabics', 'crn', 'crq',
                         'crs', 'crt', 'csk', 'cso', 'ctd', 'ctg', 'cto', 'ctu', 'cuc', 'cui', 'cuk', 'cul', 'cwa',
                         'cwe', 'cwt', 'cya', 'daa', 'dah', 'dar', 'dbj', 'dbq', 'ddn', 'ded', 'des', 'dga', 'dgi',
                         'dgk', 'dgo', 'dgr', 'dhi', 'did', 'dig', 'dik', 'dip', 'div', 'djk', 'dnj-dialect_blowowest',
                         'dnj-dialect_gweetaawueast', 'dnt', 'dnw', 'dop', 'dos', 'dsh', 'dso', 'dtp', 'dts', 'dug',
                         'dwr', 'dyi', 'dyo', 'dyu', 'dzo', 'eip', 'eka', 'emp', 'enb', 'enx', 'ese', 'ess', 'eus',
                         'evn', 'ewe', 'eza', 'fal', 'fao', 'far', 'fij', 'flr', 'fmu', 'fon', 'frd',
                         'gag-script_cyrillic', 'gag-script_latin', 'gai', 'gam', 'gau', 'gbi', 'gbk', 'gbm', 'gbo',
                         'gde', 'geb', 'gej', 'gil', 'gjn', 'gkn', 'gld', 'glk', 'gmv', 'gna', 'gnd', 'gng',
                         'gof-script_latin', 'gog', 'gor', 'gqr', 'grc', 'gri', 'grn', 'grt', 'gso', 'gub', 'guc',
                         'gud', 'guh', 'guk', 'gum', 'guo', 'guq', 'guu', 'gux', 'gvc', 'gvl', 'gwi', 'gwr', 'gym',
                         'gyr', 'had', 'hag', 'hak', 'hap', 'hat', 'hay', 'heh', 'hif', 'hig', 'hil', 'hlb', 'hlt',
                         'hne', 'hnn', 'hns', 'hoc', 'hoy', 'hto', 'hub', 'hui', 'hus-dialect_centralveracruz',
                         'hus-dialect_westernpotosino', 'huu', 'huv', 'hvn', 'hwc', 'hyw', 'iba', 'icr', 'idd', 'ifa',
                         'ifb', 'ife', 'ifk', 'ifu', 'ify', 'ign', 'ikk', 'ilb', 'ilo', 'imo', 'inb', 'iou', 'ipi',
                         'iqw', 'iri', 'irk', 'itl', 'itv', 'ixl-dialect_sangasparchajul', 'ixl-dialect_sanjuancotzal',
                         'ixl-dialect_santamarianebaj', 'izr', 'izz', 'jac', 'jam', 'jbu', 'jen', 'jic', 'jiv', 'jmc',
                         'jmd', 'jun', 'juy', 'jvn', 'kaa', 'kab', 'kac', 'kak', 'kao', 'kaq', 'kay', 'kbo', 'kbp',
                         'kbq', 'kbr', 'kby', 'kca', 'kcg', 'kdc', 'kde', 'kdh', 'kdi', 'kdj', 'kdl', 'kdn', 'kdt',
                         'kek', 'ken', 'keo', 'ker', 'key', 'kez', 'kfb', 'kff-script_telugu', 'kfw', 'kfx', 'khg',
                         'khq', 'kia', 'kij', 'kik', 'kin', 'kjb', 'kje', 'kjg', 'kjh', 'kki', 'kkj', 'kle', 'klu',
                         'klv', 'klw', 'kma', 'kmd', 'kml', 'kmr-script_arabic', 'kmr-script_cyrillic',
                         'kmr-script_latin', 'kmu', 'knb', 'kne', 'knf', 'knj', 'knk', 'kno', 'kog', 'kpq', 'kps',
                         'kpv', 'kpy', 'kpz', 'kqe', 'kqp', 'kqr', 'kqy', 'krc', 'kri', 'krj', 'krl', 'krr', 'krs',
                         'kru', 'ksb', 'ksr', 'kss', 'ktb', 'ktj', 'kub', 'kue', 'kum', 'kus', 'kvn', 'kvw', 'kwd',
                         'kwf', 'kwi', 'kxc', 'kxf', 'kxm', 'kxv', 'kyb', 'kyc', 'kyf', 'kyg', 'kyo', 'kyq', 'kyu',
                         'kyz', 'kzf', 'lac', 'laj', 'lam', 'las', 'lat', 'law', 'lbj', 'lbw', 'lcp', 'lee', 'lef',
                         'lem', 'lew', 'lex', 'lgg', 'lgl', 'lhu', 'lia', 'lid', 'lif', 'lip', 'lis', 'lje', 'ljp',
                         'llg', 'lln', 'lme', 'lnd', 'lns', 'lob', 'lok', 'lom', 'lon', 'loq', 'lsi', 'lsm', 'luc',
                         'lwo', 'lww', 'lzz', 'maa-dialect_sanantonio', 'maa-dialect_sanjeronimo', 'mad', 'mag', 'mah',
                         'mai', 'maj', 'mak', 'mam-dialect_central', 'mam-dialect_northern', 'mam-dialect_southern',
                         'mam-dialect_western', 'maq', 'maw', 'maz', 'mbb', 'mbc', 'mbh', 'mbj', 'mbt', 'mbu', 'mbz',
                         'mca', 'mcb', 'mcd', 'mco', 'mcp', 'mcq', 'mcu', 'mda', 'mdv', 'mdy', 'med', 'mee', 'mej',
                         'men', 'meq', 'met', 'mev', 'mfe', 'mfh', 'mfi', 'mfk', 'mfq', 'mfy', 'mfz', 'mgd', 'mge',
                         'mgh', 'mgo', 'mhi', 'mhr', 'mhu', 'mhx', 'mhy', 'mib', 'mie', 'mif', 'mih', 'mil', 'mim',
                         'min', 'mio', 'mip', 'miq', 'mit', 'miy', 'miz', 'mjl', 'mjv', 'mkl', 'mkn', 'mlg', 'mmg',
                         'mnb', 'mnf', 'mnk', 'mnw', 'mnx', 'moa', 'mog', 'mop', 'mor', 'mos', 'mox', 'moz', 'mpg',
                         'mpm', 'mpp', 'mpx', 'mqb', 'mqf', 'mqj', 'mqn', 'mrw', 'msy', 'mtd', 'mtj', 'mto', 'muh',
                         'mup', 'mur', 'muv', 'muy', 'mvp', 'mwq', 'mwv', 'mxb', 'mxq', 'mxt', 'mxv', 'myb', 'myk',
                         'myl', 'myv', 'myx', 'myy', 'mza', 'mzi', 'mzj', 'mzk', 'mzm', 'mzw', 'nab', 'nag', 'nan',
                         'nas', 'naw', 'nca', 'nch', 'ncj', 'ncl', 'ncu', 'ndj', 'ndp', 'ndv', 'ndy', 'ndz', 'neb',
                         'new', 'nfa', 'nfr', 'nga', 'ngl', 'ngp', 'ngu', 'nhe', 'nhi', 'nhu', 'nhw', 'nhx', 'nhy',
                         'nia', 'nij', 'nim', 'nin', 'nko', 'nlc', 'nlg', 'nlk', 'nmz', 'nnb', 'nnq', 'nnw', 'noa',
                         'nod', 'nog', 'not', 'npl', 'npy', 'nst', 'nsu', 'ntm', 'ntr', 'nuj', 'nus', 'nuz', 'nwb',
                         'nxq', 'nyf', 'nyn', 'nyo', 'nyy', 'nzi', 'obo', 'ojb-script_latin', 'ojb-script_syllabics',
                         'oku', 'old', 'omw', 'onb', 'ood', 'oss', 'ote', 'otq', 'ozm', 'pab', 'pad', 'pag', 'pam',
                         'pao', 'pap', 'pau', 'pbb', 'pbc', 'pbi', 'pce', 'pcm', 'peg', 'pez', 'pib', 'pil', 'pir',
                         'pis', 'pjt', 'pkb', 'pls', 'plw', 'pmf', 'pny', 'poh-dialect_eastern', 'poh-dialect_western',
                         'poi', 'poy', 'ppk', 'pps', 'prf', 'prk', 'prt', 'pse', 'pss', 'ptu', 'pui', 'pwg', 'pww',
                         'pxm', 'qub', 'quc-dialect_central', 'quc-dialect_east', 'quc-dialect_north', 'quf', 'quh',
                         'qul', 'quw', 'quy', 'quz', 'qvc', 'qve', 'qvh', 'qvm', 'qvn', 'qvo', 'qvs', 'qvw', 'qvz',
                         'qwh', 'qxh', 'qxl', 'qxn', 'qxo', 'qxr', 'rah', 'rai', 'rap', 'rav', 'raw', 'rej', 'rel',
                         'rgu', 'rhg', 'rif-script_arabic', 'rif-script_latin', 'ril', 'rim', 'rjs', 'rkt',
                         'rmc-script_cyrillic', 'rmc-script_latin', 'rmo', 'rmy-script_cyrillic', 'rmy-script_latin',
                         'rng', 'rnl', 'rol', 'rop', 'rro', 'rub', 'ruf', 'rug', 'run', 'sab', 'sag', 'sah', 'saj',
                         'saq', 'sas', 'sba', 'sbd', 'sbl', 'sbp', 'sch', 'sck', 'sda', 'sea', 'seh', 'ses', 'sey',
                         'sgb', 'sgj', 'sgw', 'shi', 'shk', 'shn', 'sho', 'shp', 'sid', 'sig', 'sil', 'sja', 'sjm',
                         'sld', 'slu', 'sml', 'smo', 'sne', 'snn', 'snp', 'snw', 'soy', 'spp', 'spy', 'sqi', 'sri',
                         'srm', 'srn', 'srx', 'stn', 'stp', 'suc', 'suk', 'sun', 'sur', 'sus', 'suv', 'suz', 'sxb',
                         'sxn', 'sya', 'syl', 'sza', 'tac', 'taj', 'tao', 'tap', 'taq', 'tat', 'tav', 'tbc', 'tbg',
                         'tbk', 'tbl', 'tby', 'tbz', 'tca', 'tcc', 'tcs', 'tcz', 'tdj', 'ted', 'tee', 'tem', 'teo',
                         'ter', 'tes', 'tew', 'tex', 'tfr', 'tgj', 'tgo', 'tgp', 'thk', 'thl', 'tih', 'tik', 'tir',
                         'tkr', 'tlb', 'tlj', 'tly', 'tmc', 'tmf', 'tna', 'tng', 'tnk', 'tnn', 'tnp', 'tnr', 'tnt',
                         'tob', 'toc', 'toh', 'tom', 'tos', 'tpi', 'tpm', 'tpp', 'tpt', 'trc', 'tri', 'trn', 'trs',
                         'tso', 'tsz', 'ttc', 'tte', 'ttq-script_tifinagh', 'tue', 'tuf', 'tuk-script_arabic',
                         'tuk-script_latin', 'tuo', 'tvw', 'twb', 'twe', 'twu', 'txa', 'txq', 'txu', 'tye',
                         'tzh-dialect_bachajon', 'tzh-dialect_tenejapa', 'tzj-dialect_eastern', 'tzj-dialect_western',
                         'tzo-dialect_chamula', 'tzo-dialect_chenalho', 'ubl', 'ubu', 'udm', 'udu', 'uig-script_arabic',
                         'uig-script_cyrillic', 'unr', 'upv', 'ura', 'urb', 'urd-script_devanagari', 'urd-script_latin',
                         'urk', 'urt', 'ury', 'usp', 'uzb-script_cyrillic', 'vag', 'vid', 'vif', 'vmw', 'vmy', 'vun',
                         'vut', 'wal-script_ethiopic', 'wal-script_latin', 'wap', 'war', 'waw', 'way', 'wba', 'wlo',
                         'wlx', 'wmw', 'wob', 'wsg', 'wwa', 'xal', 'xdy', 'xed', 'xer', 'xmm', 'xnj', 'xnr', 'xog',
                         'xon', 'xrb', 'xsb', 'xsm', 'xsr', 'xsu', 'xta', 'xtd', 'xte', 'xtm', 'xtn', 'xua', 'xuo',
                         'yaa', 'yad', 'yal', 'yam', 'yao', 'yas', 'yat', 'yaz', 'yba', 'ybb', 'ycl', 'ycn', 'yea',
                         'yka', 'yli', 'yre', 'yua', 'yuz', 'yva', 'zaa', 'zab', 'zac', 'zad', 'zae', 'zai', 'zam',
                         'zao', 'zaq', 'zar', 'zas', 'zav', 'zaw', 'zca', 'zga', 'zim', 'ziw', 'zmz', 'zne', 'zos',
                         'zpc', 'zpg', 'zpi', 'zpl', 'zpm', 'zpo', 'zpt', 'zpu', 'zpz', 'ztq', 'zty', 'zyb', 'zyp',
                         'zza']
    _LANGS3 = _LANGS2 + ['abk', 'bas', 'bre', 'che', 'epo', 'fry', 'hsb', 'ina', 'mdf', 'nno', 'roh-dialect_sursilv',
                         'roh-dialect_vallader', 'sat', 'srp-script_cyrillic', 'vot']

    def __init__(self, config: dict = None):
        config = config or {}
        self.model = config["model"] = config.get("model") or "facebook/mms-1b-all"
        super().__init__(config)
        self.stt = Wav2VecSTT(config=config)

    def execute(self, audio: AudioData, language: Optional[str] = None):
        return self.stt.execute(audio, language)

    @property
    def available_languages(self) -> set:
        if self.model == "facebook/mms-1b-all":  # 1162 langs
            return set(standardize_lang_tag(t) for t in self._LANGS3)
        elif self.model == "facebook/mms-1b-l1107":  # 1107 langs
            return set(standardize_lang_tag(t) for t in self._LANGS2)
        elif self.model == "facebook/mms-1b-fl102":  # 102 langs
            return set(standardize_lang_tag(t) for t in self._LANGS1)
        return set()


if __name__ == "__main__":
    b = MMSSTT({"use_cuda": True})
    print(len(b.available_languages), sorted(list(b.available_languages)))
    from speech_recognition import Recognizer, AudioFile

    eu = "/home/miro/PycharmProjects/ovos-stt-plugin-fasterwhisper/jfk.wav"
    with AudioFile(eu) as source:
        audio = Recognizer().record(source)

    a = b.execute(audio, language="gl")
    print(a)
    # ten en conta que as funcionarlidades incluídas nesta páxino ofrécense unicamente con fins de demostración se tes algún comentario subxestión ou detectas algún problema durante a demostración ponte en contacto con nosco
