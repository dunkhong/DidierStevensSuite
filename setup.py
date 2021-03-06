#! /usr/bin/env python

from distutils.core import setup

setup(name='DidierStevensiSuite',
    author='Didier Stevens',
    version='20190312',
    install_requires=[
        '',
    ],
    py_modules=[
        'plugin_biff',
        'plugin_dridex',
        'plugin_embeddedfile',
        'plugin_hifo',
        'plugin_http_heuristics',
        'plugin_jumplist',
        'plugin_linear',
        'plugin_msg',
        'plugin_msi',
        'plugin_nameobfuscation',
        'plugin_office_crypto',
        'plugin_pcode_dumper',
        'plugin_ppt',
        'plugin_str_sub',
        'plugin_stream_o',
        'plugin_stream_sample',
        'plugin_triage',
        'plugin_vba_summary',
    ],
    scripts=[
        'MIFAREACR122.py',
        'apc-b.py',
        'apc-channel.py',
        'apc-pr-log.py',
        'base64dump.py',
        'byte-stats.py',
        'cipher-tool.py',
        'cisco-calculate-ssh-fingerprint.py',
        'count.py',
        'cut-bytes.py',
        'decode-vbe.py',
        'decoder_add1.py',
        'decoder_ah.py',
        'decoder_chr.py',
        'decoder_rol1.py',
        'decoder_xor1.py',
        'decompress_rtf.py',
        'defuzzer.py',
        'disitool.py',
        'emldump.py',
        'extractscripts.py',
        'file-magic.py',
        'file2vbscript.py',
        'find-file-in-file.py',
        'format-bytes.py',
        'generate-hashcat-toggle-rules.py',
        'hash.py',
        'headtail.py',
        'hex-to-bin.py',
        'image-forensics-ela.py',
        'image-overlay.py',
        'jpegdump.py',
        'keihash.py',
        'lookup-hosts.py',
        'lookup-ips.py',
        'mPDF.py',
        'make-pdf-embedded.py',
        'make-pdf-helloworld.py',
        'make-pdf-javascript.py',
        'make-pdf-jbig2.py',
        'msoffcrypto-crack.py',
        'naft-gfe.py',
        'naft-icd.py',
        'naft-ii.py',
        'naft_iipf.py',
        'naft_impf.py',
        'naft_pfef.py',
        'naft_uf.py',
        'nmap-xml-script-output.py',
        'nsrl.py',
        'numbers-to-hex.py',
        'numbers-to-string.py',
        'oledump.py',
        'password-history-analysis.py',
        'pcap-rename.py',
        'pdf-parser.py',
        'pdfid.py',
        'pecheck.py',
        'peid-userdb-to-yara-rules.py',
        'process-binary-file.py',
        'process-text-file.py',
        'python-per-line.py',
        're-search.py',
        'reextra.py',
        'rtfdump.py',
        'sets.py',
        'setup.py',
        'shellcode2vba.py',
        'shellcode2vbscript.py',
        'simple-shellcode-generator.py',
        'split.py',
        'strings.py',
        'translate.py',
        'virustotal-search.py',
        'virustotal-submit.py',
        'vs.py',
        'what-is-new.py',
        'wsrradial.py',
        'wsrtool.py',
        'xmldump.py',
        'xor-kpa.py',
        'zipdump.py',
    ],
)
