# -*- coding: utf-8 -*-
"""
Analyse PRE (avant le coup) -> Stockfish multipv -> softmax(beta) -> H & 2^H
Sorties:
- data/run/run_info.json, data/run/engine_info.json
- data/processed/{positions,candidates,games}.csv (+ .parquet si dispo)
- data/output_tests/{positions_small,candidates_small}.csv
"""

import json, math, datetime as dt
from pathlib import Path
import numpy as np
import pandas as pd
import chess.pgn
import chess.engine
import matplotlib.pyplot as plt
# --- récupère run_id depuis le JSON que la fonction vient d’écrire ---
from pathlib import Path

# -----------------------
# Paramètres à adapter
# -----------------------
PGN_PATH = r"C:\Users\Admin\Documents\entropie-echecs\data\PGN\Magnus Carlsen_vs_Arjun Erigaisi_2024.08.08.pgn"
ENGINE_PATH = r"C:\Users\Admin\Documents\entropie-echecs\stockfish\stockfish.exe"

DEPTH = 10
MULTIPV = 10
MATE_CP = 1000                      # conversion mate -> centipions
BETA_PER_CP = 0.01                  # softmax(exp(beta * cp)) ; ici équiv. à /100
MAX_GAMES = 1                       # nombre de parties à traiter pour la démo

# -----------------------
# Utilitaires
# -----------------------
def softmax_beta(scores_cp, beta_per_cp=BETA_PER_CP):
    x = np.array(scores_cp, dtype=float) * beta_per_cp
    x -= np.max(x)                          # stabilité numérique
    ex = np.exp(x)
    s = ex.sum()
    return (ex / s).tolist(), float(s)

def shannon_entropy_bits(probs):
    p = np.array(probs, dtype=float)
    p = p[(p > 0)]
    if p.size == 0:
        return 0.0
    return float(-np.sum(p * (np.log(p) / np.log(2.0))))

def color_to_str(board):
    return "white" if board.turn else "black"

def now_run_id():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def ensure_dirs():
    for d in ["data/run", "data/processed", "data/output_tests", "data/raw"]:
        Path(d).mkdir(parents=True, exist_ok=True)

# -----------------------
# Analyse d’un PGN (PRE)
# -----------------------
def analyze_pgn_pre(pgn_path, engine_path, depth=DEPTH, multipv=MULTIPV,
                    beta_per_cp=BETA_PER_CP, mate_cp=MATE_CP, max_games=MAX_GAMES):

    ensure_dirs()
    run_id = now_run_id()

    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    engine_name = getattr(engine, "id", {}).get("name", "Unknown")
    engine_author = getattr(engine, "id", {}).get("author", None)

    positions_records, candidates_records, games_records = [], [], []

    with open(pgn_path, encoding="utf-8", errors="ignore") as f:
        for game_idx in range(max_games):
            game = chess.pgn.read_game(f)
            if game is None:
                break

            board = game.board()
            game_id = f"{Path(pgn_path).stem}__{game_idx+1}"

            headers = getattr(game, "headers", {})
            white_elo = headers.get("WhiteElo", None)
            black_elo = headers.get("BlackElo", None)
            result = headers.get("Result", None)

            ply = 0
            for mv in game.mainline_moves():
                ply += 1

                # --- PRE : analyser AVANT de pousser le coup ---
                color = color_to_str(board)
                fen_pre = board.fen()
                played_move_uci = mv.uci()

                info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=multipv)

                cps, ucis = [], []
                for entry in info:
                    cp = entry["score"].relative.score(mate_score=mate_cp)
                    pv = entry.get("pv", None)
                    if cp is None or not pv:
                        continue
                    ucis.append(pv[0].uci())
                    cps.append(int(cp))

                k_effective = len(cps)
                if k_effective == 0:
                    positions_records.append({
                        "run_id": run_id, "game_id": game_id, "ply": ply,
                        "color": color, "fen": fen_pre, "analysis_frame": "pre",
                        "depth": depth, "multipv": multipv, "beta_per_cp": beta_per_cp,
                        "k_effective": 0, "H_bits": 0.0, "n_plausible": 1.0,
                        "cp_best": None, "sum_prob": None,
                        "played_move_uci": played_move_uci, "played_in_candidates": False,
                        "played_rank": None, "played_prob": None, "delta_cp_played": None,
                        "logloss_bits": None, "top1_hit": False, "top3_hit": False, "top5_hit": False
                    })
                    board.push(mv)
                    continue

                probs, _ = softmax_beta(cps, beta_per_cp=beta_per_cp)
                sum_prob = float(np.sum(probs))
                H_bits = shannon_entropy_bits(probs)
                cp_best = int(np.max(cps))

                order = np.argsort(-np.array(cps))
                cps_sorted = np.array(cps)[order]
                ucis_sorted = np.array(ucis)[order]
                probs_sorted = np.array(probs)[order]

                played_in_candidates = played_move_uci in set(ucis_sorted.tolist())
                played_rank = played_prob = delta_cp_played = logloss_bits = None
                if played_in_candidates:
                    idx = np.where(ucis_sorted == played_move_uci)[0][0]
                    played_rank = int(idx + 1)
                    played_prob = float(probs_sorted[idx])
                    delta_cp_played = int(cps_sorted[idx] - cp_best)
                    logloss_bits = float(-math.log(played_prob, 2)) if played_prob > 0 else None

                top1_hit = bool(played_in_candidates and played_rank == 1)
                top3_hit = bool(played_in_candidates and (played_rank is not None) and played_rank <= 3)
                top5_hit = bool(played_in_candidates and (played_rank is not None) and played_rank <= 5)

                positions_records.append({
                    "run_id": run_id, "game_id": game_id, "ply": ply,
                    "color": color, "fen": fen_pre, "analysis_frame": "pre",
                    "depth": depth, "multipv": multipv, "beta_per_cp": beta_per_cp,
                    "k_effective": int(k_effective), "H_bits": float(H_bits),
                    "n_plausible": float(2.0 ** H_bits), "cp_best": int(cp_best),
                    "sum_prob": float(sum_prob),
                    "played_move_uci": played_move_uci, "played_in_candidates": bool(played_in_candidates),
                    "played_rank": None if played_rank is None else int(played_rank),
                    "played_prob": None if played_prob is None else float(played_prob),
                    "delta_cp_played": None if delta_cp_played is None else int(delta_cp_played),
                    "logloss_bits": None if logloss_bits is None else float(logloss_bits),
                    "top1_hit": bool(top1_hit), "top3_hit": bool(top3_hit), "top5_hit": bool(top5_hit)
                })

                for r, (u, cp, p) in enumerate(zip(ucis_sorted.tolist(), cps_sorted.tolist(), probs_sorted.tolist()), start=1):
                    candidates_records.append({
                        "run_id": run_id, "game_id": game_id, "ply": ply,
                        "rank": int(r), "uci": u, "cp": int(cp), "prob": float(p),
                        "delta_to_best_cp": int(cp - cp_best), "is_best": bool(r == 1),
                        "is_played": bool(u == played_move_uci)
                    })

                # maintenant seulement, on pousse le coup
                board.push(mv)

            # agrégats partie
            pos_df_tmp = pd.DataFrame([r for r in positions_records if r["game_id"] == game_id])
            if not pos_df_tmp.empty:
                games_records.append({
                    "run_id": run_id, "game_id": game_id,
                    "white_elo": white_elo, "black_elo": black_elo, "result": result,
                    "n_positions": int(len(pos_df_tmp)),
                    "H_mean_white": float(pos_df_tmp.loc[pos_df_tmp["color"]=="white","H_bits"].mean()),
                    "H_mean_black": float(pos_df_tmp.loc[pos_df_tmp["color"]=="black","H_bits"].mean()),
                    "n_plausible_mean_white": float(pos_df_tmp.loc[pos_df_tmp["color"]=="white","n_plausible"].mean()),
                    "n_plausible_mean_black": float(pos_df_tmp.loc[pos_df_tmp["color"]=="black","n_plausible"].mean()),
                    "top1_rate": float(pos_df_tmp["top1_hit"].mean(skipna=True)),
                    "top3_rate": float(pos_df_tmp["top3_hit"].mean(skipna=True)),
                    "top5_rate": float(pos_df_tmp["top5_hit"].mean(skipna=True))
                })

    try:
        engine.quit()
    except Exception:
        pass

    # Écritures
    positions_df = pd.DataFrame(positions_records)
    candidates_df = pd.DataFrame(candidates_records)
    games_df = pd.DataFrame(games_records)

    positions_df.to_csv("data/processed/positions.csv", index=False)
    candidates_df.to_csv("data/processed/candidates.csv", index=False)
    games_df.to_csv("data/processed/games.csv", index=False)

    try:
        positions_df.to_parquet("data/processed/positions.parquet", index=False)
        candidates_df.to_parquet("data/processed/candidates.parquet", index=False)
    except Exception:
        pass

    positions_df.head(30).to_csv("data/output_tests/positions_small.csv", index=False)
    candidates_df.head(300).to_csv("data/output_tests/candidates_small.csv", index=False)

    run_info = {
        "run_id": run_id,
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "script": "entropy_pre.py",
        "source_pgn": str(pgn_path),
        "analysis_frame": "pre",
        "depth": depth,
        "multipv": multipv,
        "beta_per_cp": beta_per_cp,
        "notes": "demo public pre-frame"
    }
    engine_info = {
        "engine_name": engine_name,
        "engine_author": engine_author,
        "engine_path": str(engine_path),
        "options": { "Threads": 1, "Hash": 256 },
        "mate_cp_policy": f"mate_score={mate_cp}"
    }
    with open("data/run/run_info.json", "w", encoding="utf-8") as f:
        json.dump(run_info, f, ensure_ascii=False, indent=2)
    with open("data/run/engine_info.json", "w", encoding="utf-8") as f:
        json.dump(engine_info, f, ensure_ascii=False, indent=2)

    return positions_df, candidates_df, games_df




def make_figures(positions_df: pd.DataFrame, run_id: str, project_root: Path):
    fig_dir = (project_root / "figures" / "runs" / run_id)
    fig_dir.mkdir(parents=True, exist_ok=True)

    # 1) H par demi-coup (PRE)
    plt.figure()
    plt.plot(positions_df["ply"], positions_df["H_bits"], marker='o')
    plt.xlabel("Ply (demi-coup)")
    plt.ylabel("Entropie H (bits)")
    plt.title("Évolution de H par demi-coup (cadre PRE)")
    plt.tight_layout()
    plt.savefig(fig_dir / f"H_per_ply_{run_id}.png")
    plt.close()

    # 2) Top-1 par quartiles de H (sur positions avec k_effective>0)
    qpos = positions_df[positions_df["k_effective"] > 0].copy()
    if not qpos.empty:
        q1, q2, q3 = qpos["H_bits"].quantile([0.25, 0.5, 0.75]).tolist()
        def qbin(h):
            if h <= q1: return "Q1 (faible H)"
            elif h <= q2: return "Q2"
            elif h <= q3: return "Q3"
            else: return "Q4 (forte H)"
        qpos["H_quartile"] = qpos["H_bits"].apply(qbin)
        top1_by_q = qpos.groupby("H_quartile")["top1_hit"].mean().reindex(
            ["Q1 (faible H)","Q2","Q3","Q4 (forte H)"]
        )
        plt.figure()
        top1_by_q.plot(kind="bar")
        plt.ylabel("Taux Top-1")
        plt.title("Top-1 par quartiles d'entropie (PRE)")
        plt.tight_layout()
        plt.savefig(fig_dir / f"top1_by_quartile_{run_id}.png")
        plt.close()

    # 3) Scatter H vs log-loss (positions où le coup joué est dans les candidats)
    mask = (positions_df["played_in_candidates"]==True) & positions_df["logloss_bits"].notna()
    if mask.sum() >= 2:
        x = positions_df.loc[mask, "H_bits"].astype(float).values
        y = positions_df.loc[mask, "logloss_bits"].astype(float).values
        plt.figure()
        plt.scatter(x, y, s=25)
        # régression linéaire simple pour lisibilité
        m, c = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 100)
        ys = m*xs + c
        plt.plot(xs, ys)
        r = np.corrcoef(x, y)[0,1]
        plt.xlabel("H (bits)")
        plt.ylabel("Log-loss (bits) du coup joué")
        plt.title(f"H vs Log-loss (r = {r:.3f})")
        plt.tight_layout()
        plt.savefig(fig_dir / f"H_vs_logloss_{run_id}.png")
        plt.close()

    # 4) 2^H par couleur avec zones d'interprétation
    dfw = positions_df[positions_df["color"]=="white"].copy()
    dfb = positions_df[positions_df["color"]=="black"].copy()
    # numéro de coup (1,2,3,...) = ceil(ply/2)
    dfw["move_no"] = ((dfw["ply"] + 1)//2).astype(int)
    dfb["move_no"] = ((dfb["ply"] + 1)//2).astype(int)
    dfw["choices"] = (2.0 ** dfw["H_bits"])
    dfb["choices"] = (2.0 ** dfb["H_bits"])
    ymax = float(max(dfw["choices"].max() if not dfw.empty else 4,
                     dfb["choices"].max() if not dfb.empty else 4, 4)) + 1.0

    plt.figure(figsize=(12,6))
    # zones

    plt.axhspan(4, ymax, facecolor='green', alpha=0.10,
            label='♞ Liberté stratégique (> 4 choix)')
    plt.axhspan(2, 4, facecolor='gold',  alpha=0.15,
                label='♟ Choix restreints (2–4 choix)')   
    plt.axhspan(1.3, 2, facecolor='darkorange', alpha=0.15,
                label='⚠ Dilemme (≈ 2 choix)')            
    plt.axhspan(0, 1.3, facecolor='red', alpha=0.12,
                label='☠ Coup quasi forcé (≤ 1.3)')       #

    if not dfw.empty:
        plt.plot(dfw["move_no"], dfw["choices"], marker='o', linestyle='-', label='Blancs')
    if not dfb.empty:
        plt.plot(dfb["move_no"], dfb["choices"], marker='x', linestyle='--', label='Noirs')

    plt.xlabel("Numéro du coup")
    plt.ylabel("Nombre de coups plausibles (≈ 2^H)")
    plt.title("Évolution stratégique par joueur (cadre PRE)")
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_dir / f"choices_by_color_{run_id}.png")
    plt.close()

# --- lance l’analyse et récupère les DataFrames ---
positions_df, candidates_df, games_df = analyze_pgn_pre(PGN_PATH, ENGINE_PATH)


with open(Path("data/run/run_info.json"), encoding="utf-8") as f:
    run_info = json.load(f)

# --- racine du projet (si ton script est à la racine, parent() suffit) ---
PROJECT_ROOT = Path(__file__).resolve().parent

# --- génère et enregistre les figures ---
make_figures(positions_df, run_info["run_id"], PROJECT_ROOT)

