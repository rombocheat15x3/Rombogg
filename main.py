import os, sys, time, json, binascii, base64, random, re, requests, socket, threading, urllib3, psutil, jwt, pickle, asyncio, logging
import xKEys
from datetime import datetime
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, ContextTypes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf import descriptor as _descriptor, descriptor_pool as _descriptor_pool, symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from protobuf_decoder.protobuf_decoder import Parser

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8036720168:AAEwNrPKkxxLdubasJPUbNNZ9Gy-CPcWBtw")
BOT_USERNAME = "rombo_hack_bot"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10my_message.proto\">\n\tMyMessage\x12\x0f\n\x07\x66ield21\x18\x15 \x01(\x03\x12\x0f\n\x07\x66ield22\x18\x16 \x01(\x0c\x12\x0f\n\x07\x66ield23\x18\x17 \x01(\x0c\x62\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'my_message_pb2', _globals)
MyMessage = _globals['MyMessage']

def EnC_AEs(HeX):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()

def DEc_AEs(HeX):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return unpad(cipher.decrypt(bytes.fromhex(HeX)), AES.block_size).hex()

def EnC_PacKeT(HeX, K, V):
    return AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(HeX), 16)).hex()

def DEc_PacKeT(HeX, K, V):
    return unpad(AES.new(K, AES.MODE_CBC, V).decrypt(bytes.fromhex(HeX)), 16).hex()

def EnC_Uid(H, Tp='Uid'):
    e, H = [], int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0))
        H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None

def EnC_Vr(N):
    if N < 0:
        return b''
    H = []
    while True:
        b = N & 0x7F
        N >>= 7
        if N:
            b |= 0x80
        H.append(b)
        if not N:
            break
    return bytes(H)

def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not (b & 0x80):
            break
        s += 7
    return n

def DecodE_HeX(H):
    return hex(H)[2:].zfill(2)

def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))
        elif isinstance(value, (str, bytes)):
            packet.extend(CrEaTe_LenGTh(field, value))
    return packet

# مرادفات للتوافق
create_protobuf_packet = CrEaTe_ProTo
encrypt_packet = EnC_PacKeT
dec_to_hex = DecodE_HeX
get_random_avatar = lambda: xBunnEr()
def ArA_CoLor():
    Tp = ["32CD32", "00BFFF", "00FA9A", "90EE90", "FF4500", "FF6347",
          "FF69B4", "FF8C00", "FF6347", "FFD700", "FFDAB9", "F0F0F0",
          "F0E68C", "D3D3D3", "A9A9A9", "D2691E", "CD853F", "BC8F8F",
          "6A5ACD", "483D8B", "4682B4", "9370DB", "C71585", "FF8C00", "FFA07A"]
    return random.choice(Tp)

def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {'wire_type': result.wire_type}
        if result.wire_type in ("varint", "string", "bytes"):
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def DeCode_PackEt(input_text):
    try:
        parsed = Parser().parse(input_text)
        return json.dumps(Fix_PackEt(parsed))
    except Exception as e:
        print(f"error {e}")
        return None

def _V(b, i):
    r = s = 0
    while True:
        c = b[i]
        i += 1
        r |= (c & 0x7F) << s
        if c < 0x80:
            break
        s += 7
    return r, i

def PrOtO(hx):
    b, i, R = bytes.fromhex(hx), 0, {}
    while i < len(b):
        H, i = _V(b, i)
        F, T = H >> 3, H & 7
        if T == 0:
            R[F], i = _V(b, i)
        elif T == 2:
            L, i = _V(b, i)
            S = b[i:i+L]
            i += L
            try:
                R[F] = S.decode()
            except:
                try:
                    R[F] = PrOtO(S.hex())
                except:
                    R[F] = S
        elif T == 5:
            R[F] = int.from_bytes(b[i:i+4], 'little')
            i += 4
        else:
            raise ValueError(f'Unknown wire type: {T}')
    return R

def GeT_KEy(obj, target):
    values = []
    def collect(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == target:
                    values.append(v)
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)
    collect(obj)
    return values[-1] if values else None

def xMsGFixinG(n):
    return '🗿'.join(str(n)[i:i+3] for i in range(0, len(str(n)), 3))

def xBunnEr():
    avatars = [
        902000306, 902000305, 902000003, 902000016, 902000017, 902000019,
        902000020, 902000021, 902000023, 902000070, 902000087, 902000108,
        902000011, 902049020, 902049018, 902049017, 902049016, 902049015,
        902049003, 902033016, 902033017, 902033018, 902048018, 902000306, 902000305
    ]
    return random.choice(avatars)

def Ua():
    TmP = "GarenaMSDK/4.0.13 ({}; {}; {};)"
    return TmP.format(
        random.choice(["iPhone 13 Pro", "iPhone 14", "iPhone XR", "Galaxy S22", "Note 20", "OnePlus 9", "Mi 11"]),
        random.choice(["iOS 17", "iOS 18", "Android 13", "Android 14"]),
        random.choice(["en-SG", "en-US", "fr-FR", "id-ID", "th-TH", "vi-VN"])
    )

def GeT_Time(timestamp):
    last = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    diff = now - last
    days = diff.days
    hours, rem = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return days, hours, minutes, seconds

def Time_En_Ar(t):
    return t.replace("Day", "يوم").replace("Hour", "ساعة").replace("Min", "دقيقة").replace("Sec", "ثانية")

def GeneRaTePk(Pk, N, K, V):
    PkEnc = EnC_PacKeT(Pk, K, V)
    _ = DecodE_HeX(len(PkEnc) // 2)
    if len(_) == 2:
        HeadEr = N + "000000"
    elif len(_) == 3:
        HeadEr = N + "00000"
    elif len(_) == 4:
        HeadEr = N + "0000"
    elif len(_) == 5:
        HeadEr = N + "000"
    else:
        HeadEr = N + "000000"
    return bytes.fromhex(HeadEr + _ + PkEnc)

def xSEndMsg(Msg , Tp , Tp2 , id , K , V):
    feilds = {1: id, 2: Tp2, 3: Tp, 4: Msg , 5: 1735129800, 7: 2, 9: {1: "fadai", 2: xBunnEr(), 3: 901048018, 4: 330, 5: 909034009, 8: "fadai", 10: 1, 11: 1, 14: {1: 1158053040, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"}}, 10: "en", 13: {2: 1, 3: 1}, 14: {}}
    Pk = str(CrEaTe_ProTo(feilds).hex())
    Pk = "080112" + EnC_Uid(len(Pk) // 2 , Tp = 'Uid') + Pk
    return GeneRaTePk(str(Pk) , '1215' , K , V)

def Auth_Chat(idT, sq, K, V):
    fields = {
        1: 3,
        2: {
            1: idT,
            3: "fr",
            4: sq
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '1215' , K , V)
    
def OpEnSq(K , V):
    fields = {1: 1, 2: {2: "\u0001", 3: 1, 4: 1, 5: "en", 9: 1, 11: 1, 13: 1, 14: {2: 5756, 6: 11, 8: "1.111.5", 9: 2, 10: 4}}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def spmroom(K, V, uid):
    fields = {
        1: 22,     
        2: {       
            1: int(uid)  
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0E15', K, V)



def openroom(K, V):
    fields = {
        1: 2,  
        2: {   
            1: 1,  
            2: 15, 
            3: 5,
            4: "MASRY_CORE",
            5: "1",
            6: 12,
            7: 1,
            8: 1,
            9: 1,
            11: 1,
            12: 2,
            14: 36981056,
            15: {
                1: "IDC3",
                2: 126,
                3: "ME"
            },
            16: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000f\u000e\u0016\u0019\u001a \u001d",
            18: 2368584,
            27: 1,
            34: "\u0000\u0001",
            40: "en",
            48: 1,
            49: {
                1: 21
            },
            50: {
                1: 36981056,
                2: 2368584,
                5: 2
            }
        }
    }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()), '0E15', K, V)
    
def cHSq(Nu , Uid , K , V):
    fields = {1: 17, 2: {1: int(Uid), 2: 1, 3: int(Nu - 1), 4: 62, 5: "\u001a", 8: 5, 13: 329}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)

def SEnd_InV(Nu , Uid , K , V):
    fields = {1: 2 , 2: {1: int(Uid) , 2: "ME" , 4: int(Nu)}}
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)
    
def ExiT(id , K , V):
    fields = {
        1: 7,
        2: {
            1: int(11037044965)
        }
        }
    return GeneRaTePk(str(CrEaTe_ProTo(fields).hex()) , '0515' , K , V)


def AuthClan(CLan_Uid, AuTh, K, V):
    fields = {1: 3, 2: {1: int(CLan_Uid), 2: 1, 4: str(AuTh)}}
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '1201', K, V)

def GeT_Status(PLayer_Uid, K, V):
    PLayer_Uid = EnC_Uid(PLayer_Uid, 'Uid')
    if len(PLayer_Uid) == 8:
        Pk = f'080112080a04{PLayer_Uid}1005'
    elif len(PLayer_Uid) == 10:
        Pk = f"080112090a05{PLayer_Uid}1005"
    else:
        Pk = f'080112080a04{PLayer_Uid}1005'
    return GeneRaTePk(Pk, '0f15', K, V)

def MaSrY_SpM(Uid, Rm, Nm, K, V):
    fields = {
        1: 2,
        2: {
            1: 1, 2: 15, 3: 5, 4: Nm, 5: Rm, 6: 12, 7: 1, 8: 1, 9: 1,
            11: 1, 12: 2, 14: int(Uid),
            15: {1: "IDC3", 2: 126, 3: "ME"},
            16: "\u0001\u0003\u0004\u0007\t\n\u000b\u0012\u000f\u000e\u0016\u0019\u001a \u001d",
            18: int(Rm), 27: 1, 34: "\u0000\u0001", 40: "en", 48: 1,
            49: {1: 21},
            50: {1: int(Uid), 2: int(Rm), 5: 2}
        }
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0E15', K, V)

def SPMR1(Uid, K, V):
    fields = {1: 22, 2: {1: int(Uid)}}
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0E15', K, V)

def SPam_Room(Uid, Rm, Nm, K, V):
    fields = {
        1: 78,
        2: {
            1: int(Rm), 2: f"[{ArA_CoLor()}]{Nm}",
            3: {2: 1, 3: 1}, 4: 330, 5: 1, 6: 201,
            10: xBunnEr(), 11: int(Uid), 12: 1
        }
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0e15', K, V)

def Join_Room(room_id, K, V):
    fields = {
        1: 3,
        2: {
            1: int(room_id),
            8: {1: "IDC1", 2: 3000, 3: "ME"},
            9: "\x01\t\n\x12\x19 ",
            10: 1,
            12: b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01",
            13: 3, 14: 3, 16: "ME"
        }
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0e10', K, V)

def SPamSq(Uid, K, V):
    fields = {
        1: 33,
        2: {
            1: int(Uid), 2: 'ME', 3: 1, 4: 1, 7: 330, 8: 19459, 9: 100,
            12: 1, 16: 1,
            17: {2: 94, 6: 11, 8: '1.111.5', 9: 3, 10: 2},
            18: 201, 23: {2: 1, 3: 1}, 24: xBunnEr(), 26: {}, 28: {}
        }
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0515', K, V)

async def Emote_k(TarGeT, idT, K, V, region):
    fields = {
        1: 21,
        2: {
            1: 804266360,
            2: 909000001,
            5: {1: TarGeT, 3: idT}
        }
    }
    pkt_type = '0515'
    if region.lower() == "ind":
        pkt_type = '0514'
    elif region.lower() == "bd":
        pkt_type = "0519"
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), pkt_type, K, V)

def AccEpT(PLayer_Uid, AuTh_CodE_Sq, K, V):
    fields = {
        1: 4,
        2: {
            1: int(PLayer_Uid), 3: int(PLayer_Uid),
            4: "\u0001\u0007\t\n\u0012\u0019\u001a ", 8: 1,
            9: {2: 1393, 4: "wW_T", 6: 11, 8: "1.111.5", 9: 3, 10: 2},
            10: AuTh_CodE_Sq, 12: 1, 13: "en", 16: "OR"
        }
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0515', K, V)

def GenJoinSquadsPacket(code, key, iv):
    fields = {
        1: 4,
        2: {
            4: bytes.fromhex("01090a0b121920"),
            5: str(code),
            6: 6,
            8: 1,
            9: {2: 800, 6: 11, 8: "1.111.1", 9: 5, 10: 1}
        }
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0515', key, iv)

def MaSrY_ToP(player_id, key, iv):
    fields = {
        1: 5,
        2: {1: int(player_id), 2: 1, 3: int(player_id),
            4: "[b][c][FF0000]▒█▀▀█ ░█▀█░ 　"}
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0515', key, iv)

def XR(player_id, key, iv):
    fields = {
        1: int(player_id),
        2: 5,
        4: 50,
        5: {1: int(player_id), 2: "[00FF00]RoMboo_CORE BOT V1", 3: 1}
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0515', key, iv)

def xGeT(u, p):
    print(f"جار توليد التوكن لـ UID: {u}")
    try:
        r = requests.Session().post(
            "https://100067.connect.garena.com/oauth/guest/token/grant",
            headers={
                "Host": "100067.connect.garena.com",
                "User-Agent": Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close"
            },
            data={
                "uid": u,
                "password": p,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067"
            },
            verify=False
        )
        if r.status_code == 200:
            T = r.json()
            print("تم الحصول على التوكن بنجاح من Garena")
            a, o = T["access_token"], T["open_id"]
            jwt_token = xJwT(a, o)
            if jwt_token:
                print("تم توليد JWT بنجاح")
                return jwt_token
            else:
                print("فشل في توليد JWT")
                return None
        else:
            print(f"خطأ في الاستجابة من Garena: {r.status_code}")
            return None
    except Exception as e:
        print(f"حدث خطأ في xGeT: {str(e)}")
        return None

def xJwT(a, o):
    try:
        dT = bytes.fromhex(
            '1a13323032352d31302d33312030353a31383a3235220966726565206669726528013a07312e3131382e344232416e64726f6964204f532039202f204150492d3238202850492f72656c2e636a772e32303232303531382e313134313333294a0848616e6468656c64520c4d544e2f537061636574656c5a045749464960800a68d00572033234307a2d7838362d3634205353453320535345342e3120535345342e32204156582041565832207c2032343030207c20348001e61e8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e329a012b476f6f676c657c36323566373136662d393161372d343935622d396631362d303866653964336336353333a2010d3137362e32382e3133352e3233aa01026172b201203433303632343537393364653836646134323561353263616164663231656564ba010134c2010848616e6468656c64ca010d4f6e65506c7573204135303130ea014034653739616666653331343134393031353434656161626562633437303537333866653638336139326464346335656533646233333636326232653936363466f00101ca020c4d544e2f537061636574656cd2020457494649ca03203161633462383065636630343738613434323033626638666163363132306635e003b5ee02e803ff8502f003af13f803840780048c95028804b5ee0290048c95029804b5ee02b00404c80401d2043d2f646174612f6170702f636f6d2e6474732e667265656669726574682d66705843537068495636644b43376a4c2d574f7952413d3d2f6c69622f61726de00401ea045f65363261623933353464386662356662303831646233333861636233333439317c2f646174612f6170702f636f6d2e6474732e667265656669726574682d66705843537068495636644b43376a4c2d574f7952413d3d2f626173652e61706bf00406f804018a050233329a050a32303139313139303236a80503b205094f70656e474c455332b805ff01c00504e005c466ea05093372645f7061727479f80583e4068806019006019a060134a2060134b2062211541141595f58011f53594c59584056143a5f535a525c6b5c04096e595c3b000e61'
        )
        dT = dT.replace(b'2025-07-30 14:11:20', str(datetime.now())[:-7].encode())
        dT = dT.replace(b'4e79affe31414901544eaabebc4705738fe683a92dd4c5ee3db33662b2e9664f', a.encode())
        dT = dT.replace(b'4306245793de86da425a52caadf21eed', o.encode())
        PyL = bytes.fromhex(EnC_AEs(dT.hex()))
        r = requests.Session().post(
            "https://loginbp.ggwhitehawk.com/MajorLogin",
            headers={
                "Expect": "100-continue",
                "X-Unity-Version": "2018.4.11f1",
                "X-GA": "v1 1",
                "ReleaseVersion": "OB52",
                "Authorization": "Bearer ",
                "Host": "loginbp.ggwhitehawk.com"
            },
            data=PyL,
            verify=False
        )
        if r.status_code == 200:
            response_data = json.loads(DeCode_PackEt(binascii.hexlify(r.content).decode('utf-8')))
            return response_data['8']['data']
        else:
            print(f"خطأ في MajorLogin: {r.status_code}")
            return None
    except Exception as e:
        print(f"حدث خطأ في xJwT: {str(e)}")
        return None

def L_DaTa():
    def load(f):
        return json.load(open(f)) if os.path.exists(f) else {}
    return map(load, ["BesTo_CLan_LiKes.json", "BesTo_RemaininG_LiKes.json", "BesTo_RemaininG_Room.json"])

like_data_clan, like_data, room_data = L_DaTa()

def ChEck_Limit_CLan(Uid, STaTus):
    if STaTus != "like":
        return False, ""
    data = like_data_clan
    max_use = 10
    file = "BesTo_CLan_LiKes.json"
    t = time.time()
    limit = 86400
    u = data.get(str(Uid), {"count": 0, "start_time": t})
    if t - u["start_time"] >= limit:
        u = {"count": 0, "start_time": t}
    if u["count"] < max_use:
        u["count"] += 1
        data[str(Uid)] = u
        json.dump(data, open(file, "w"))
        remain = max_use - u["count"]
        expire = datetime.fromtimestamp(u["start_time"] + limit).strftime("%I:%M %p - %d/%m/%y")
        return remain, expire
    expire = datetime.fromtimestamp(u["start_time"] + limit).strftime("%I:%M %p - %d/%m/%y")
    return False, expire

def ChEck_Limit(Uid, STaTus):
    if STaTus == "like":
        data, max_use, file = like_data, 10, "BesTo_RemaininG_LiKes.json"
    else:
        data, max_use, file = room_data, 10, "BesTo_RemaininG_Room.json"
    t = time.time()
    limit = 86400
    u = data.get(str(Uid), {"count": 0, "start_time": t})
    if t - u["start_time"] >= limit:
        u = {"count": 0, "start_time": t}
    if u["count"] < max_use:
        u["count"] += 1
        data[str(Uid)] = u
        json.dump(data, open(file, "w"))
        remain = max_use - u["count"]
        expire = datetime.fromtimestamp(u["start_time"] + limit).strftime("%I:%M %p - %d/%m/%y")
        return remain, expire
    expire = datetime.fromtimestamp(u["start_time"] + limit).strftime("%I:%M %p - %d/%m/%y")
    return False, expire

def GuiLd_AccEss(Tg, Nm, Uid, BLk, OwN, AprV):
    return Tg in Nm and Uid not in BLk and Uid in (OwN | AprV)

def ChEck_Commande(id):
    return "<" not in id and ">" not in id and "[" not in id and "]" not in id

class FF_CLient():

    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.key = None
        self.iv = None
        self.Get_FiNal_ToKen_0115()     
            
    def Connect_SerVer_OnLine(self , Token , tok , host , port , key , iv , host2 , port2):
            try:
                self.AutH_ToKen_0115 = tok    
                self.CliEnts2 = socket.create_connection((host2 , int(port2)))
                self.CliEnts2.send(bytes.fromhex(self.AutH_ToKen_0115))                  
            except:pass        
            while True:
                try:
                    self.DaTa2 = self.CliEnts2.recv(99999)
                    if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:	         	    	    
                            self.packet = json.loads(DeCode_PackEt(f'08{self.DaTa2.hex().split("08", 1)[1]}'))
                            self.AutH = self.packet['5']['data']['7']['data']
                    
                except:pass    	
                                                            
    def Connect_SerVer(self , Token , tok , host , port , key , iv , host2 , port2):
            self.AutH_ToKen_0115 = tok    
            self.CliEnts = socket.create_connection((host , int(port)))
            self.CliEnts.send(bytes.fromhex(self.AutH_ToKen_0115))  
            self.DaTa = self.CliEnts.recv(1024)          	        
            threading.Thread(target=self.Connect_SerVer_OnLine, args=(Token , tok , host , port , key , iv , host2 , port2)).start()
            self.Exemple = xMsGFixinG('12345678')
            
            
            self.key = key
            self.iv = iv
            
            
            with connected_clients_lock:
                connected_clients[self.id] = self
                print(f" تم تسجيل الحساب {self.id} في القائمة العالمية، عدد الحسابات الآن: {len(connected_clients)}")
            
            while True:      
                try:
                    self.DaTa = self.CliEnts.recv(1024)   
                    if len(self.DaTa) == 0 or (hasattr(self, 'DaTa2') and len(self.DaTa2) == 0):	            		
                        try:            		    
                            self.CliEnts.close()
                            if hasattr(self, 'CliEnts2'):
                                self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)                    		                    
                        except:
                            try:
                                self.CliEnts.close()
                                if hasattr(self, 'CliEnts2'):
                                    self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                            except:
                                self.CliEnts.close()
                                if hasattr(self, 'CliEnts2'):
                                    self.CliEnts2.close()
                                ResTarT_BoT()	            
                                      
        	 	 
                                                               
                    if '/pp/' in self.input_msg[:4]:
                        self.target_id = self.input_msg[4:]	 
                        self.Zx = ChEck_Commande(self.target_id)
                        if True == self.Zx:	            		     
                            
                            threading.Thread(target=send_spam_from_all_accounts, args=(self.target_id,)).start()
                            time.sleep(2.5)    			         
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] SuccEss Spam To {xMsGFixinG(self.target_id)} From All Accounts\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(1.3)
                            self.CliEnts.close()
                            if hasattr(self, 'CliEnts2'):
                                self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	            		      	
                        elif False == self.Zx: 
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /pp/<id>\n - Ex : /pp/{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	
                            time.sleep(1.1)
                            self.CliEnts.close()
                            if hasattr(self, 'CliEnts2'):
                                self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	            		

                except Exception as e:
                    print(f"Error in Connect_SerVer: {e}")
                    try:
                        self.CliEnts.close()
                        if hasattr(self, 'CliEnts2'):
                            self.CliEnts2.close()
                    except:
                        pass
                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                    
    def GeT_Key_Iv(self , serialized_data):
        my_message = xKEys.MyMessage()
        my_message.ParseFromString(serialized_data)
        timestamp , key , iv = my_message.field21 , my_message.field22 , my_message.field23
        timestamp_obj = Timestamp()
        timestamp_obj.FromNanoseconds(timestamp)
        timestamp_seconds = timestamp_obj.seconds
        timestamp_nanos = timestamp_obj.nanos
        combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
        return combined_timestamp , key , iv    

    def Guest_GeneRaTe(self, uid, password):
        import requests
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close",
        }
        data = {
            "uid": f"{uid}",
            "password": f"{password}",
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067",
        }
        try:
            resp = requests.post(url, headers=headers, data=data).json()
            self.Access_ToKen, self.Access_Uid = resp['access_token'], resp['open_id']
            time.sleep(0.2)
            print(f' - Uid : {uid}\n - Password : {password}')
            #print(f' - Access Token : {self.Access_ToKen}\n - Access Id : {self.Access_ToKenAccess_ToKenAccess_ToKen}')
            return self.ToKen_GeneRaTe(self.Access_ToKen, self.Access_Uid)
        except Exception as e:
            print(f"Error in Guest_GeneRaTe: {e}")
            time.sleep(10)
            return self.Guest_GeneRaTe(uid, password)

    def GeT_LoGin_PorTs(self, JwT_ToKen, PayLoad):
        import requests
        url = 'https://clientbp.ggpolarbear.com/GetLoginData'
        headers = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JwT_ToKen}',
            'X-Unity-Version': '2022.3.47f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
            'Host': 'clientbp.ggpolarbear.com',
            'Connection': 'close',
            'Accept-Encoding': 'deflate, gzip',
        }
        try:
            res = requests.post(url, headers=headers, data=PayLoad, verify=False)
            data = json.loads(DeCode_PackEt(res.content.hex()))
            addr1, addr2 = data['32']['data'], data['14']['data']
            ip1, port1 = addr1[:-6], addr1[-5:]
            ip2, port2 = addr2[:-6], addr2[-5:]
            return ip1, port1, ip2, port2
        except requests.RequestException:
            print(" - Bad Requests !")
        print(" - Failed To GeT PorTs !")
        return None, None, None, None

    def ToKen_GeneRaTe(self, Access_ToKen, Access_Uid):
        import requests
        url = "https://loginbp.ggpolarbear.com/MajorLogin"
        headers = {
            'X-Unity-Version': '2022.3.47f1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'User-Agent': 'UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
            'Host': 'loginbp.ggpolarbear.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'deflate, gzip'
        }

        dT = bytes.fromhex(
            '1a13323032352d31312d32362030313a35313a3238220966726565206669726528013a07312e3132302e314232416e64726f6964204f532039202f204150492d3238202850492f72656c2e636a772e32303232303531382e313134313333294a0848616e6468656c64520c4d544e2f537061636574656c5a045749464960800a68d00572033234307a2d7838362d3634205353453320535345342e3120535345342e32204156582041565832207c2032343030207c20348001e61e8a010f416472656e6f2028544d292036343092010d4f70656e474c20455320332e329a012b476f6f676c657c36323566373136662d393161372d343935622d396631362d303866653964336336353333a2010e3137362e32382e3133392e313835aa01026172b201203433303632343537393364653836646134323561353263616164663231656564ba010134c2010848616e6468656c64ca010d4f6e65506c7573204135303130ea014063363961653230386661643732373338623637346232383437623530613361316466613235643161313966616537343566633736616334613065343134633934f00101ca020c4d544e2f537061636574656cd2020457494649ca03203161633462383065636630343738613434323033626638666163363132306635e003b5ee02e8039a8002f003af13f80384078004a78f028804b5ee029004a78f029804b5ee02b00404c80401d2043d2f646174612f6170702f636f6d2e6474732e667265656669726574682d66705843537068495636644b43376a4c2d574f7952413d3d2f6c69622f61726de00401ea045f65363261623933353464386662356662303831646233333861636233333439317c2f646174612f6170702f636f6d2e6474732e667265656669726574682d66705843537068495636644b43376a4c2d574f7952413d3d2f626173652e61706bf00406f804018a050233329a050a32303139313139303236a80503b205094f70656e474c455332b805ff01c00504e005be7eea05093372645f7061727479f205704b717348543857393347646347335a6f7a454e6646775648746d377171316552554e6149444e67526f626f7a4942744c4f695943633459367a767670634943787a514632734f453463627974774c7334785a62526e70524d706d5752514b6d654f35766373386e51594268777148374bf805e7e4068806019006019a060134a2060134b2062213521146500e590349510e460900115843395f005b510f685b560a6107576d0f0366'
        )

        dT = dT.replace(b'2025-07-30 14:11:20', str(datetime.now())[:-7].encode())
        dT = dT.replace(b'c69ae208fad72738b674b2847b50a3a1dfa25d1a19fae745fc76ac4a0e414c94', Access_ToKen.encode())
        dT = dT.replace(b'4306245793de86da425a52caadf21eed', Access_Uid.encode())

        try:
            hex_data = dT.hex()
            encoded_data = EnC_AEs(hex_data)
            if not all(c in '0123456789abcdefABCDEF' for c in encoded_data):
                encoded_data = hex_data
            payload = bytes.fromhex(encoded_data)
        except Exception as e:
            print(f" Error in encoding: {e}")
            payload = dT

        resp = requests.post(url, headers=headers, data=payload, verify=False)
        if resp.status_code == 200 and len(resp.text) > 10:
            try:
                data = json.loads(DeCode_PackEt(resp.content.hex()))
                jwt_token = data['8']['data']
                combined_ts, key, iv = self.GeT_Key_Iv(resp.content)
                ip, port, ip2, port2 = self.GeT_LoGin_PorTs(jwt_token, payload)
                return jwt_token, key, iv, combined_ts, ip, port, ip2, port2
            except Exception as e:
                print(f" Error parsing response: {e}")
                time.sleep(5)
                return self.ToKen_GeneRaTe(Access_ToKen, Access_Uid)
        else:
            print(f" Error in ToKen_GeneRaTe, status: {resp.status_code}")
            time.sleep(5)
            return self.ToKen_GeneRaTe(Access_ToKen, Access_Uid)

    def Get_FiNal_ToKen_0115(self):
        try:
            result = self.Guest_GeneRaTe(self.id, self.password)
            if not result:
                print(" Failed to get tokens, retrying...")
                time.sleep(5)
                return self.Get_FiNal_ToKen_0115()

            token, key, iv, ts, ip, port, ip2, port2 = result
            if not all([ip, port, ip2, port2]):
                print(" Failed to get ports, retrying...")
                time.sleep(5)
                return self.Get_FiNal_ToKen_0115()

            self.JwT_ToKen = token
            try:
                decoded = jwt.decode(token, options={"verify_signature": False})
                self.AccounT_Uid = decoded.get('account_id')
                self.EncoDed_AccounT = hex(self.AccounT_Uid)[2:]
                self.HeX_VaLue = DecodE_HeX(ts)
                self.TimE_HEx = self.HeX_VaLue
                self.JwT_ToKen_ = token.encode().hex()
                print(f' ProxCed Uid : {self.AccounT_Uid}')
            except Exception as e:
                #print(f" Error In ToKen : {e}")
                time.sleep(5)
                return self.Get_FiNal_ToKen_0115()

            try:
                header_len = len(EnC_PacKeT(self.JwT_ToKen_, key, iv)) // 2
                len_hex = DecodE_HeX(header_len)
                uid_len = len(self.EncoDed_AccounT)
                zeros = {
                    7: '000000000',
                    8: '00000000',
                    9: '0000000',
                    10: '000000'
                }.get(uid_len, '00000000')
                self.Header = f'0115{zeros}{self.EncoDed_AccounT}{self.TimE_HEx}00000{len_hex}'
                self.FiNal_ToKen_0115 = self.Header + EnC_PacKeT(self.JwT_ToKen_, key, iv)
            except Exception as e:
                #print(f" Error In Final Token : {e}")
                time.sleep(5)
                return self.Get_FiNal_ToKen_0115()

            self.AutH_ToKen = self.FiNal_ToKen_0115
            self.Connect_SerVer(self.JwT_ToKen, self.AutH_ToKen, ip, port, key, iv, ip2, port2)
            return self.AutH_ToKen, key, iv

        except Exception as e:
            #print(f" Error in Get_FiNal_ToKen_0115: {e}")
            time.sleep(10)
            return self.Get_FiNal_ToKen_0115()

connected_clients = {}
connected_clients_lock = threading.Lock()

active_spam_targets = {}
active_spam_lock = threading.Lock()

def spam_worker(target_id, duration_minutes=None):
    print(f"بدء السبام على الهدف: {target_id}" + (f" لمدة {duration_minutes} دقيقة" if duration_minutes else ""))
    start = datetime.now()
    while True:
        with active_spam_lock:
            if target_id not in active_spam_targets:
                print(f"توقف السبام على الهدف: {target_id}")
                break
            if duration_minutes:
                elapsed = (datetime.now() - start).total_seconds()
                if elapsed >= duration_minutes * 60:
                    print(f"انتهت مدة السبام على الهدف: {target_id}")
                    del active_spam_targets[target_id]
                    break
        try:
            send_spam_from_all_accounts(target_id)
            time.sleep(0.1)
        except Exception as e:
            print(f"خطأ في السبام على {target_id}: {e}")
            time.sleep(1)

def spam_worker(target_id, duration_minutes=None):
    print(f" بدء السبام على الهدف: {target_id}" + (f" لمدة {duration_minutes} دقيقة" if duration_minutes else ""))
    
    start_time = datetime.now()
    
    while True:
        with active_spam_lock:
            if target_id not in active_spam_targets:
                print(f"️ توقف السبام على الهدف: {target_id}")
                break
                
            
            if duration_minutes:
                elapsed = datetime.now() - start_time
                if elapsed.total_seconds() >= duration_minutes * 60:
                    print(f" انتهت مدة السبام على الهدف: {target_id}")
                    del active_spam_targets[target_id]
                    break
                
        try:
            send_spam_from_all_accounts(target_id)
            time.sleep(0.1)  
        except Exception as e:
            print(f" خطأ في السبام على {target_id}: {e}")
            time.sleep(1)

import time

def send_spam_from_all_accounts(target_id):
    while True:  # يخلي السبام يشتغل كل دقيقة
        with connected_clients_lock:
            for account_id, client in connected_clients.items():
                try:
                    if (hasattr(client, 'CliEnts2') and client.CliEnts2 and 
                        hasattr(client, 'key') and client.key and 
                        hasattr(client, 'iv') and client.iv):

                        try:
                            client.CliEnts2.send(openroom(client.key, client.iv))
                            print(f"فتح الروم من الحساب: {account_id}")
                        except Exception as e:
                            print(f"خطأ في فتح الروم من الحساب {account_id}: {e}")

                        for i in range(10):
                            try:
                                client.CliEnts2.send(spmroom(client.key, client.iv, target_id))
                                print(f"إرسال سبام من الحساب {account_id} إلى {target_id} - {i+1}")
                                
                                time.sleep(2)  # مهم جدًا (تأخير بين كل رسالة)

                            except (BrokenPipeError, ConnectionResetError, OSError) as e:
                                print(f"خطأ اتصال للحساب {account_id}: {e}")
                                break
                            except Exception as e:
                                print(f"خطأ في الإرسال من الحساب {account_id}: {e}")
                                break
                    else:
                        print(f"اتصال الحساب {account_id} غير نشط")

                except Exception as e:
                    print(f"خطأ في الحساب {account_id}: {e}")

        print("استنى دقيقة قبل الجولة الجاية...")
        time.sleep(60)  # هنا بقى السبام بالدقايق

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = "https://iili.io/fLOk0ge.jpg"
    caption = (
        "<b>مرحباً بك في بوت RoMboo15x3 للتحكم في سبام Free Fire!</b>\n\n"
        "<b>الأوامر المتاحة:</b>\n"
        "/spam &lt;user_id&gt; [duration] - بدء السبام (duration بالدقائق اختياري)\n"
        "/stop &lt;user_id&gt; - إيقاف السبام\n"
        "/status - عرض حالة النظام\n"
        "/accounts - عرض الحسابات المتصلة"
    )
    await update.message.reply_photo(photo=photo_url, caption=caption, parse_mode='HTML')

async def spam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if not args:
            await update.message.reply_text("يرجى إدخال user_id. مثال: /spam 13983449300 5")
            return
        
        target_id = args[0]
        duration = int(args[1]) if len(args) > 1 else None

        if not ChEck_Commande(target_id):
            await update.message.reply_text("user_id غير صالح!")
            return

        with active_spam_lock:
            if target_id in active_spam_targets:
                await update.message.reply_text(f"السبام يعمل بالفعل على المستخدم: {target_id}")
                return
            active_spam_targets[target_id] = {
                'active': True,
                'start_time': datetime.now(),
                'duration': duration
            }
            threading.Thread(target=spam_worker, args=(target_id, duration), daemon=True).start()

        msg = f"تم بدء السبام على المستخدم: {target_id}"
        if duration:
            msg += f" لمدة {duration} دقيقة"
        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"خطأ: {str(e)}")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if not args:
            await update.message.reply_text("يرجى إدخال user_id. مثال: /stop 13983449300")
            return
        
        target_id = args[0]
        with active_spam_lock:
            if target_id in active_spam_targets:
                del active_spam_targets[target_id]
                await update.message.reply_text(f"تم إيقاف السبام على المستخدم: {target_id}")
            else:
                await update.message.reply_text(f"لا يوجد سبام نشط على المستخدم: {target_id}")

    except Exception as e:
        await update.message.reply_text(f"خطأ: {str(e)}")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with active_spam_lock:
        active = list(active_spam_targets.keys())
        active_info = []
        for tid in active:
            data = active_spam_targets[tid]
            if data['duration']:
                elapsed = (datetime.now() - data['start_time']).total_seconds()
                remaining = data['duration'] * 60 - elapsed
                if remaining > 0:
                    active_info.append(f"• {tid} (متبقي {int(remaining/60)} دقيقة)")
                else:
                    active_info.append(f"• {tid}")
            else:
                active_info.append(f"• {tid} (بدون مدة)")
    with connected_clients_lock:
        acc_count = len(connected_clients)
        acc_list = list(connected_clients.keys())

    msg = (
        f"<b>حالة النظام</b>\n\n"
        f"<b>الأهداف النشطة:</b> {len(active)}\n"
        + ("\n".join(active_info) if active_info else "لا يوجد أهداف نشطة") +
        f"\n\n<b>الحسابات المتصلة:</b> {acc_count}\n"
        + ("\n".join([f"• {aid}" for aid in acc_list]) if acc_list else "لا توجد حسابات متصلة")
    )
    await update.message.reply_text(msg, parse_mode='HTML')

async def accounts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with connected_clients_lock:
        acc_count = len(connected_clients)
        acc_list = list(connected_clients.keys())
    msg = f"<b>الحسابات المتصلة:</b> {acc_count}\n"
    msg += "\n".join([f"• {aid}" for aid in acc_list]) if acc_list else "لا توجد حسابات متصلة"
    await update.message.reply_text(msg, parse_mode='HTML')

def load_accounts_from_file(filename="MaSrY.txt"):
    accounts = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    parts = line.split(":")
                    accounts.append({'id': parts[0].strip(), 'password': parts[1].strip()})
                else:
                    accounts.append({'id': line, 'password': ''})
       # print(f"تم تحميل {len(accounts)} حساب من {filename}")
    except FileNotFoundError:
        print(f"ملف {filename} غير موجود!")
    return accounts

ACCOUNTS = load_accounts_from_file()

def start_account(account):
    try:
        print(f" Starting account: {account['id']}")
        FF_CLient(account['id'], account['password'])
    except Exception as e:
        print(f" Error starting account {account['id']}: {e}")
        time.sleep(5)
        start_account(account)  

def run_accounts():
    for acc in ACCOUNTS:
        threading.Thread(target=start_account, args=(acc,), daemon=True).start()
        time.sleep(3)

def main():
    accounts_thread = threading.Thread(target=run_accounts, daemon=True)
    accounts_thread.start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spam", spam_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("accounts", accounts_command))

    print("sh8al nikomk w9")
    application.run_polling()

if __name__ == "__main__":
    main()