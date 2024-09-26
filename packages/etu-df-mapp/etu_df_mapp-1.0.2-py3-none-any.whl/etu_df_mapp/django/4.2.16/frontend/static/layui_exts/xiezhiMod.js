/**
 * xiezhiMod 模块，主要是自定义的 layui 模块功能，提供
 **/
layui.define(function(exports){ // 也可以依赖其他模块
  let obj = {
    // 检查 session_key 是否存在，不存在则跳转到指定url
    checkSessionKey: function(session_key, url){
      // 检查请求的cookies是否有session_key
      if (!session_key) {
        window.location.href = url // 跳转到登录
      }
    }
  };

  // 输出 xiezhiMod 接口
  exports('xiezhiMod', obj);
});