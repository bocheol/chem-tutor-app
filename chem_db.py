# chem_db.py

CHEM_DB = {
    # -------------------------------------------------------------------------
    # [1] 기본 수소 화합물 및 할로젠/주기율표 교환 분자 (1, 2번 규칙)
    # -------------------------------------------------------------------------
    # 산소(O) / 황(S) 계열 (굽은형)
    "H2O":  {"smiles": "O", "angle": "104.5°", "shape": "굽은형"},
    "OF2":  {"smiles": "FOF", "angle": "103°", "shape": "굽은형"},
    "OCl2": {"smiles": "ClOCl", "angle": "111°", "shape": "굽은형"},
    "OBr2": {"smiles": "BrOBr", "angle": "약 104.5°", "shape": "굽은형"},
    "H2S":  {"smiles": "S", "angle": "92°", "shape": "굽은형"},
    "SF2":  {"smiles": "FSF", "angle": "98°", "shape": "굽은형"},
    "SCl2": {"smiles": "ClSCl", "angle": "103°", "shape": "굽은형"},
    "SBr2": {"smiles": "BrSBr", "angle": "약 104.5°", "shape": "굽은형"},

    # 질소(N) / 인(P) 계열 (삼각뿔형)
    "NH3":  {"smiles": "N", "angle": "107°", "shape": "삼각뿔형"},
    "NF3":  {"smiles": "FN(F)F", "angle": "102°", "shape": "삼각뿔형"},
    "NCl3": {"smiles": "ClN(Cl)Cl", "angle": "107°", "shape": "삼각뿔형"},
    "NBr3": {"smiles": "BrN(Br)Br", "angle": "약 107°", "shape": "삼각뿔형"},
    "PH3":  {"smiles": "P", "angle": "93°", "shape": "삼각뿔형"},
    "PF3":  {"smiles": "FP(F)F", "angle": "98°", "shape": "삼각뿔형"},
    "PCl3": {"smiles": "ClP(Cl)Cl", "angle": "100°", "shape": "삼각뿔형"},
    "PBr3": {"smiles": "BrP(Br)Br", "angle": "101°", "shape": "삼각뿔형"},

    # 탄소(C) / 규소(Si) 계열 (정사면체형)
    "CH4":  {"smiles": "C", "angle": "109.5°", "shape": "정사면체형"},
    "CF4":  {"smiles": "FC(F)(F)F", "angle": "109.5°", "shape": "정사면체형"},
    "CCl4": {"smiles": "ClC(Cl)(Cl)Cl", "angle": "109.5°", "shape": "정사면체형"},
    "CBr4": {"smiles": "BrC(Br)(Br)Br", "angle": "109.5°", "shape": "정사면체형"},
    "SiH4": {"smiles": "[SiH4]", "angle": "109.5°", "shape": "정사면체형"},
    "SiF4": {"smiles": "F[Si](F)(F)F", "angle": "109.5°", "shape": "정사면체형"},
    "SiCl4": {"smiles": "Cl[Si](Cl)(Cl)Cl", "angle": "109.5°", "shape": "정사면체형"},
    "SiBr4": {"smiles": "Br[Si](Br)(Br)Br", "angle": "109.5°", "shape": "정사면체형"},

    # 붕소(B) 계열 (평면삼각형)
    "BH3":  {"smiles": "[BH3]", "angle": "120°", "shape": "평면삼각형"},
    "BF3":  {"smiles": "FB(F)F", "angle": "120°", "shape": "평면삼각형"},
    "BCl3": {"smiles": "ClB(Cl)Cl", "angle": "120°", "shape": "평면삼각형"},
    "BBr3": {"smiles": "BrB(Br)Br", "angle": "120°", "shape": "평면삼각형"},

    # 베릴륨(Be) 계열 (직선형)
    "BeH2":  {"smiles": "[BeH2]", "angle": "180°", "shape": "직선형"},
    "BeF2":  {"smiles": "F[Be]F", "angle": "180°", "shape": "직선형"},
    "BeCl2": {"smiles": "Cl[Be]Cl", "angle": "180°", "shape": "직선형"},
    "BeBr2": {"smiles": "Br[Be]Br", "angle": "180°", "shape": "직선형"},

    # 이원자 분자류 (직선형, 결합각 없음)
    "H2":   {"smiles": "[H][H]", "angle": "N/A", "shape": "직선형"},
    "HF":   {"smiles": "F", "angle": "N/A", "shape": "직선형"},
    "HCl":  {"smiles": "Cl", "angle": "N/A", "shape": "직선형"},
    "HBr":  {"smiles": "Br", "angle": "N/A", "shape": "직선형"},
    "HI":   {"smiles": "I", "angle": "N/A", "shape": "직선형"},
    "F2":   {"smiles": "FF", "angle": "N/A", "shape": "직선형"},
    "Cl2":  {"smiles": "ClCl", "angle": "N/A", "shape": "직선형"},
    "Br2":  {"smiles": "BrBr", "angle": "N/A", "shape": "직선형"},
    "N2":   {"smiles": "N#N", "angle": "N/A", "shape": "직선형"},
    "O2":   {"smiles": "O=O", "angle": "N/A", "shape": "직선형"},

    # 이산화탄소 류
    "CO2":  {"smiles": "O=C=O", "angle": "180°", "shape": "직선형"},
    "CS2":  {"smiles": "S=C=S", "angle": "180°", "shape": "직선형"},

    # -------------------------------------------------------------------------
    # [2] 3번 규칙 다원자 분자 및 이온류 추가
    # -------------------------------------------------------------------------
    "COF2": {"smiles": "O=C(F)F", "angle": "약 120°", "shape": "평면삼각형"},
    "FCN":  {"smiles": "FC#N", "angle": "180°", "shape": "직선형"},
    "FNO":  {"smiles": "FN=O", "angle": "약 110°", "shape": "굽은형"},
    "CH2O": {"smiles": "C=O", "angle": "약 120°", "shape": "평면삼각형"},
    "HCN":  {"smiles": "C#N", "angle": "180°", "shape": "직선형"},
    
    # 탄소-탄소 다중결합 및 플루오린 화합물
    "C2F6": {"smiles": "FC(F)(F)C(F)(F)F", "angle": "109.5°", "shape": "사면체형(각 탄소)"},
    "C2F4": {"smiles": "FC(F)=C(F)F", "angle": "120°", "shape": "평면형"},
    "C2F2": {"smiles": "FC#CF", "angle": "180°", "shape": "직선형"},
    
    # 질소/산소 다량체 플루오린 화합물
    "N2F4": {"smiles": "FN(F)N(F)F", "angle": "약 102°", "shape": "삼각뿔형(각 질소)"},
    "N2F2": {"smiles": "FN=NF", "angle": "약 110°", "shape": "굽은형"},
    "O2F2": {"smiles": "FOOF", "angle": "약 109.5°", "shape": "굽은형"},
    
    # 다원자 이온 (대괄호 필수 표기)
    "NH4+": {"smiles": "[NH4+]", "angle": "109.5°", "shape": "정사면체형"},
    "H3O+": {"smiles": "[OH3+]", "angle": "107°", "shape": "삼각뿔형"},
}