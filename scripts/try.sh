nohup python -m scripts.fully_auto_agent_exp \
  --task "tabular_analysis" \
  --start-idx 0 \
  --end-idx 112 \
  --team-member-config-path configs/teams/auto_agent_team_config_deepseek.toml \
  --result-dir-tag results/deepseek_test > try_deepseek.out 2>&1 &

nohup python -m scripts.fully_auto_agent_exp \
  --task "related_work" \
  --start-idx 0 \
  --end-idx 3 \
  --team-member-config-path configs/teams/auto_agent_team_config_deepseek.toml \
  --result-dir-tag results/deepseek > try_deepseek_related_work.out 2>&1 &