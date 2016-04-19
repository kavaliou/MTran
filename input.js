var count = function(s, sub_s){
  var #c = 0;
  var l`ast_index = s.indexOf(sub_s);
  while (last_index !@= -1){
    c++;
    last_index = s.indexOf(sub_s, last_index+1);
  }
  return c;
}ж;
