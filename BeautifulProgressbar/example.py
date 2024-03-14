import os,progressbar
pbar_w=[progressbar.Percentage(),progressbar.GranularBar(left="(",right=")"),progressbar.ETA(format="%(eta)8s",format_finished="%(elapsed)8s",format_na="     N/A",format_not_started="--:--:--",format_zero="00:00:00")]
pbar=progressbar.ProgressBar(widgets=pbar_w,max_error=False,
  min_value=0,
  max_value=100,
  )
pbar.start()
  pbar.term_width=os.get_terminal_size()[0]
  pbar.update(i)
pbar.finish()
