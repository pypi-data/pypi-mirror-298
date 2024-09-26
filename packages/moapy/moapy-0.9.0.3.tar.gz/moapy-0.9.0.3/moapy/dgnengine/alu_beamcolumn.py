import base64
from moapy.auto_convert import auto_schema
from moapy.data_pre import MemberForce, EffectiveLength
from moapy.steel_pre import SteelSection, SteelLength
from moapy.alu_pre import AluMaterial, AluMomentModificationFactor
from moapy.dgnengine.base import generate_report_xls, load_dll
from moapy.data_post import ResultBytes

def read_file_as_binary(file_path: str) -> bytes:
    """
    주어진 경로의 파일을 바이너리 데이터로 읽어 반환합니다.

    :param file_path: 읽을 파일의 경로
    :return: 파일의 바이너리 데이터
    """
    if isinstance(file_path, bytes):
        file_path = file_path.decode('utf-8')

    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()
        return binary_data
    except Exception as e:
        print(f"파일을 읽는 중 오류 발생: {e}")
        return None

@auto_schema
def report_aluminum_beam_column(matl: AluMaterial, sect: SteelSection, load: MemberForce, length: SteelLength, eff_len: EffectiveLength, factor: AluMomentModificationFactor) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), load.json(), length.json(), eff_len.json(), factor.json()]
    file_path = generate_report_xls(dll, 'Report_Aluminum_BeamColumn', json_data_list)
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

# res = report_aluminum_beam_column(AluMaterial(), SteelSection(), MemberForce(), SteelLength(), EffectiveLength(), AluMomentModificationFactor())
# res.dict()
# print(res)
