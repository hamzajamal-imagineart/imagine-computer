const Q=c=>`/footer-cta/frames/frame-${String(c+1).padStart(4,"0")}.jpg`,g=document.querySelector("[data-cta-section]"),e=document.querySelector("[data-cta-canvas]"),C=document.querySelector("[data-cta-overlay]");if(!g||!e||!C)throw new Error("FooterCta: missing elements");g.style.height="calc(100vh + 700px)";let j=!1;const K=c=>{c!==j&&(j=c,C.dataset.revealed=c?"true":"false")},t=e.getContext("webgl");if(t){const c=`
      attribute vec2 a_pos;
      attribute vec2 a_uv;
      varying vec2 vUv;
      uniform vec2 uRes;
      uniform vec2 uTexSize;

      vec2 coverUv(vec2 uv, vec2 ts, vec2 rs) {
        vec2 r = vec2(
          min((rs.x / rs.y) / (ts.x / ts.y), 1.0),
          min((rs.y / rs.x) / (ts.y / ts.x), 1.0)
        );
        return vec2(uv.x * r.x + (1.0 - r.x) * 0.5,
                    uv.y * r.y + (1.0 - r.y) * 0.5);
      }

      void main() {
        vUv = coverUv(vec2(a_uv.x, 1.0 - a_uv.y), uTexSize, uRes);
        gl_Position = vec4(a_pos, 0.0, 1.0);
      }
    `,U=`
      precision highp float;
      varying vec2 vUv;
      uniform sampler2D uTex;
      void main() {
        gl_FragColor = texture2D(uTex, vUv);
      }
    `,A=(n,E)=>{const l=t.createShader(E);return t.shaderSource(l,n),t.compileShader(l),l},a=t.createProgram();t.attachShader(a,A(c,t.VERTEX_SHADER)),t.attachShader(a,A(U,t.FRAGMENT_SHADER)),t.linkProgram(a),t.useProgram(a),t.bindBuffer(t.ARRAY_BUFFER,t.createBuffer()),t.bufferData(t.ARRAY_BUFFER,new Float32Array([-1,-1,0,0,1,-1,1,0,-1,1,0,1,1,1,1,1]),t.STATIC_DRAW);const d=t.getAttribLocation(a,"a_pos"),h=t.getAttribLocation(a,"a_uv");t.enableVertexAttribArray(d),t.enableVertexAttribArray(h),t.vertexAttribPointer(d,2,t.FLOAT,!1,16,0),t.vertexAttribPointer(h,2,t.FLOAT,!1,16,8);const f=t.getUniformLocation(a,"uRes");t.uniform1i(t.getUniformLocation(a,"uTex"),0),t.uniform2f(t.getUniformLocation(a,"uTexSize"),1920,1080);const L=t.createTexture();t.bindTexture(t.TEXTURE_2D,L),t.texParameteri(t.TEXTURE_2D,t.TEXTURE_MIN_FILTER,t.LINEAR),t.texParameteri(t.TEXTURE_2D,t.TEXTURE_MAG_FILTER,t.LINEAR),t.texParameteri(t.TEXTURE_2D,t.TEXTURE_WRAP_S,t.CLAMP_TO_EDGE),t.texParameteri(t.TEXTURE_2D,t.TEXTURE_WRAP_T,t.CLAMP_TO_EDGE),t.texImage2D(t.TEXTURE_2D,0,t.RGB,1,1,0,t.RGB,t.UNSIGNED_BYTE,new Uint8Array([13,13,13]));const r=()=>{const n=Math.min(window.devicePixelRatio||1,2);e.width=Math.round(e.clientWidth*n),e.height=Math.round(e.clientHeight*n),t.viewport(0,0,e.width,e.height),t.uniform2f(f,e.width,e.height)};r();const s=[];let T=!1,o=-1;const _=()=>{if(!T)return;const n=g.getBoundingClientRect(),l=Math.min(Math.max(-n.top,0),600)/600,R=Math.min(144,Math.max(0,Math.round(l*144)));if(R!==o){const u=s[R];if(u?.complete&&u.naturalWidth>0)t.texImage2D(t.TEXTURE_2D,0,t.RGB,t.RGB,t.UNSIGNED_BYTE,u),o=R;else for(let m=R;m>=0;m--){const v=s[m];if(v?.complete&&v.naturalWidth>0){t.texImage2D(t.TEXTURE_2D,0,t.RGB,t.RGB,t.UNSIGNED_BYTE,v),o=m;break}}}t.drawArrays(t.TRIANGLE_STRIP,0,4),K(l>=.88)};for(let n=0;n<145;n++){const E=new Image;E.src=Q(n),s.push(E),n===0&&E.addEventListener("load",()=>{T=!0,_()},{once:!0})}const i=()=>{_(),requestAnimationFrame(i)};requestAnimationFrame(i),window.addEventListener("resize",()=>{r(),o=-1,_()})}else{const c=e.getContext("2d");if(c){const U=()=>{const r=Math.min(window.devicePixelRatio||1,2);e.width=Math.round(e.clientWidth*r),e.height=Math.round(e.clientHeight*r)};U();const A=[];let a=!1,d=-1;const h=r=>{const s=e.width,T=e.height,o=r.naturalWidth||1920,_=r.naturalHeight||1080,i=Math.max(s/o,T/_);c.clearRect(0,0,s,T),c.drawImage(r,(s-o*i)/2,(T-_*i)/2,o*i,_*i)},f=()=>{if(!a)return;const r=g.getBoundingClientRect(),T=Math.min(Math.max(-r.top,0),600)/600,o=Math.min(144,Math.max(0,Math.round(T*144)));if(o!==d){const _=A[o];if(_?.complete&&_.naturalWidth>0)h(_),d=o;else for(let i=o;i>=0;i--){const n=A[i];if(n?.complete&&n.naturalWidth>0){h(n),d=i;break}}}K(T>=.88)};for(let r=0;r<145;r++){const s=new Image;s.src=Q(r),A.push(s),r===0&&s.addEventListener("load",()=>{a=!0,f()},{once:!0})}const L=()=>{f(),requestAnimationFrame(L)};requestAnimationFrame(L),window.addEventListener("resize",()=>{U(),d=-1,f()})}}const b=document.querySelector("[data-cta-content]");if(g&&b&&e&&C&&window.matchMedia("(pointer: fine)").matches){let n=0,E=0,l=0,R=0,u=0,m=0,v=0,X=0,G=0,w=0,O=1,H="",W="",q="",z=performance.now(),V=!1,F=!1;const N=b.querySelector("button, a");N&&(N.addEventListener("mouseenter",()=>{F=!0},{passive:!0}),N.addEventListener("mouseleave",()=>{F=!1},{passive:!0}),N.addEventListener("focus",()=>{F=!0},{passive:!0}),N.addEventListener("blur",()=>{F=!1},{passive:!0})),window.addEventListener("mousemove",x=>{const M=g.getBoundingClientRect(),P=M.width/2,y=M.height/2;if(P<=0||y<=0)return;const p=Math.max(-1,Math.min(1,(x.clientX-(M.left+P))/P)),I=Math.max(-1,Math.min(1,(x.clientY-(M.top+y))/y));n=p,E=I,l=-I*2,R=p*3.5,z=performance.now(),V=!0},{passive:!0});const $=x=>{const M=x-z,P=V?Math.max(0,Math.min(1,(M-1400)/800)):1;O+=((F?0:P)-O)*.08;const p=O,I=Math.sin(x*42e-5)*.6,k=Math.sin(x*31e-5+1.1)*.4,S=(ot,at)=>ot*(1-p)+at*p,Z=S(n,I),J=S(E,k),tt=S(l,-k*2),et=S(R,I*3.5);u+=(Z-u)*.08,m+=(J-m)*.08,G+=(tt-G)*.08,w+=(et-w)*.08,e.style.transform=`scale(1.14) rotateX(${G.toFixed(3)}deg) rotateY(${w.toFixed(3)}deg) translateZ(0)`;const nt=u*6,rt=m*4;v+=(nt-v)*.055,X+=(rt-X)*.055;const D=`translate3d(${v.toFixed(2)}px,${X.toFixed(2)}px,0)`;D!==H&&(b.style.transform=D,H=D);const Y=u.toFixed(3),B=m.toFixed(3);Y!==W&&(C.style.setProperty("--mm-nx",Y),W=Y),B!==q&&(C.style.setProperty("--mm-ny",B),q=B),requestAnimationFrame($)};requestAnimationFrame($)}
