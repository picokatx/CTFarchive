#!/usr/bin/env python3

import re
from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long, long_to_bytes
from utils import listener
from pkcs1 import emsa_pkcs1_v15
# from params import N, E, D

FLAG = "crypto{?????????????????????????????????}"

MSG = 'We are hyperreality and Jack and we own CryptoHack.org'
DIGEST = emsa_pkcs1_v15.encode(MSG.encode(), 256)
# SIGNATURE = pow(bytes_to_long(DIGEST), D, N)
SIGNATURE = 16240222270498692025963397327189194914186759237776075999464894124673676202168406293551264617188443991760125496417050643646394332912181570558216262726969063702994049661909903440834938825182904653381794725535440344839391613387669481038012235273006241462239610006309243325799374858562879339721474181202813441789421308660082359229296945383245835120520267434365173357729371625932003278958544143834828992201713760808477670490533374230071254672009364681985991266985556524967416179328197312866725294051113968507425678433774457134172561405246958809795955201013662228331896312017340852384764229288525108749448398056255920050839
N = 10826017069878645400727755999235136003903416920168174188295821038773919839147771043015405269042652889278667845637798637887716889466122925983469939829156480504433718543140787080835369873663688161568130278067968162696613489895172620062094378772686883697604319597903485846393638153408522460354619110965051516030399411670998825078412503334161390916851600466615561004837627289597318734287141769569578675947074707130339210036012517552534775446413293616722862279332739418900563546893933394256325041268733599700925021163994783882378431871007329541991992106832350088481475626779975723071126769170273329728748911641177338847608
E = 65537

class Challenge():
    def __init__(self):
        self.before_input = "This server validates domain ownership with RSA signatures. Present your message and public key, and if the signature matches ours, you must own the domain.\n"

    def challenge(self, your_input):
        if not 'option' in your_input:
            return {"error": "You must send an option to this server"}

        elif your_input['option'] == 'get_signature':
            return {
                "N": hex(N),
                "e": hex(E),
                "signature": hex(SIGNATURE)
            }

        elif your_input['option'] == 'verify':
            msg = your_input['msg']
            n = int(your_input['N'], 16)
            e = int(your_input['e'], 16)

            digest = emsa_pkcs1_v15.encode(msg.encode(), 256)
            calculated_digest = pow(SIGNATURE, e, n)
            print("digest: "+str(bytes_to_long(digest)))
            print("calculated_digest: "+str(calculated_digest))
            if bytes_to_long(digest) == calculated_digest:
                r = re.match(r'^I am Mallory.*own CryptoHack.org$', msg)
                if r:
                    return {"msg": f"Congratulations, here's a secret: {FLAG}"}
                else:
                    return {"msg": f"Ownership verified."}
            else:
                return {"error": "Invalid signature"}

        else:
            return {"error": "Invalid option"}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13391)
