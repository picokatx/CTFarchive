const __func__ = [
    'exports',
    '270328ewawLo',
    'instantiate',
    '1OsuamQ',
    'Incorrect!',
    'length',
    'copy_char',
    'value',
    '1512517ESezaM',
    'innerHTML',
    'check_flag',
    'result',
    '1383842SQRPPf',
    '924408cukzgO',
    'getElementById',
    '418508cLDohp',
    'input',
    'Correct!',
    '573XsMMHp',
    'arrayBuffer',
    '183RUQBDE',
    '38934oMACea'
  ];
  const func_call = function (func_idx) {
    func_idx = func_idx - 285;
    let func = __func__[func_idx];
    return func;
  };
  (
    // timewaster
    function (const___func__, const_970828) {
      const loc_func_call = func_call;
      while (!![]) {
        try {
          //867616078
          const _0x5e2d0a = - parseInt(loc_func_call(290)) + - parseInt(loc_func_call(303)) + - parseInt(loc_func_call(294)) * - parseInt(loc_func_call(299)) 
          + - parseInt(loc_func_call(306)) + parseInt(loc_func_call(292)) + - parseInt(loc_func_call(289)) * - parseInt(loc_func_call(287)) + parseInt(loc_func_call(304));
          // out = -parseInt(5 + - 18 +- 9 *- 14 +- 21 + 7 +- 14 *- 2 + 19)
          // ['38934oMACea' '1383842SQRPPf '1OsuamQ' '1512517ESezaM'
          // '418508cLDohp' '270328ewawLo' '1512517ESezaM' '573XsMMHp'
          // '924408cukzgO']
          if (_0x5e2d0a === const_970828) break;
           else const___func__['push'](const___func__['shift']());
        } catch (_0x289152) {
          const___func__['push'](const___func__['shift']());
        }
      }
    }(__func__, 970828)
  );
  // generate exports
  let exports;
  (
    async() => {
      const loc_func_call = func_call;
      let wasm_bin = await fetch('./wasm3'),
      // wasm_obj = await WebAssembly['instantiate'](await wasm_bin['arrayBuffer']()),
      wasm_obj = await WebAssembly[loc_func_call(293)](await wasm_bin[loc_func_call(288)]()),
      wasm_funcs = wasm_obj['instance'];
      // wasm_funcs['exports']
      exports = wasm_funcs[loc_func_call(291)];
    }
  ) ();
  function onButtonPress() {
    const loc_func_call = func_call;
    let input_chars = document[loc_func_call(305)](loc_func_call(285)) [loc_func_call(298)];
    for (let i = 0; i < input_chars[loc_func_call(296)]; i++) {
      exports[loc_func_call(297)](input_chars['charCodeAt'](i), i);
    }
    exports[loc_func_call(297)](0, input_chars[loc_func_call(296)]),
    exports[loc_func_call(301)]() == 1 ? document[loc_func_call(305)](loc_func_call(302)) [loc_func_call(300)] = loc_func_call(286) : document[loc_func_call(305)](loc_func_call(302)) ['innerHTML'] = loc_func_call(295);
  }


  // exports: wasm functions
  // function onButtonPress() {
  //   input_chars = document.getElementById('input')['value'];
  //   for (let i = 0; i < input_chars.length; i++) {
  //       1<-0
  //       exports.copy_char(input_chars.charCodeAt(i), i); 
  //       
  //   }
  //   exports.copy_char(0, input_chars.length),
  //   if (exports.check_flag() == 1) {
  //       document.getElementById("result").innerHTML = 'Correct!';
  //   } else {
  //       document.getElementById("result").innerHTML = 'Incorrect!';
  //   }
  // }