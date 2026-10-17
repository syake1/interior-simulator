(() => {
 'use strict';
 const data = document.getElementById('pricing-calculator-data');
 if (!data) return;
 const items = JSON.parse(data.textContent);
 const root = document.querySelector('.pricing-calculator');
 const form = root.querySelector('form');
 const rows = root.querySelector('#calculator-rows');
 const protection = root.querySelector('#calc-protection');
 const total = root.querySelector('#calculator-total');
 const count = root.querySelector('#calculator-count');
 const wasteSummary=document.createElement('section'); wasteSummary.className='calculator-auto-waste';
 wasteSummary.innerHTML='<p class="calculator-waste-total"></p><details class="calculator-waste-details"><summary>処分費の内訳を見る</summary><ul></ul></details>';
 form.after(wasteSummary);
 const disposalRates=items.filter(item=>item.group==='waste');
 function disposalFor(item,row,quantity) {
  const index=items.filter(i=>i.group===item.group).indexOf(item);
  if(item.group==='wall'&&index===4 || !['wall','floor'].includes(item.group)) return null;
  const scope=row.querySelector('.calculator-scope').value;
  if(!scope) return {pending:true};
  if(scope==='other') return {unknown:true};
  const rateIndex=item.group==='wall'?{new:0,small:1,room:2,ldk:3}[scope]:{small:4,room:5,skirting:7}[scope];
  const rate=disposalRates[rateIndex];
  if(!rate) return {unknown:true};
  return {rate,multiplier:item.unit==='室'?quantity:1};
 }
 const groups = {wall:'壁紙・クロス工事',floor:'床工事・巾木',waste:'産業廃棄物処分費',protection:'現場養生費'};
 const yen = value => Math.round(value).toLocaleString('ja-JP')+'円';
 let serial = 0;
 function calculate() {
  let low=0, high=0, included=0, invalid=false, incomplete=false, pendingScope=false, unknownWaste=false,wasteLow=0,wasteHigh=0;
  const disposalLines=[];
  for (const row of rows.children) {
   const excluded=row.dataset.group==='protection'&&!protection.checked;
   row.classList.toggle('calculator-excluded',excluded);
   row.querySelector('select').disabled=excluded;
   row.querySelector('input[type="number"]').disabled=excluded;
   const item=items.find(i=>i.id===row.querySelector('select').value);
   const input=row.querySelector('.calculator-quantity');
   const extra=row.querySelector('.calculator-extra-area');
   const roomCount=row.querySelector('.calculator-room-count');
   const subtotal=row.querySelector('.calculator-subtotal');
   const error=row.querySelector('.calculator-error');
   error.textContent=''; input.removeAttribute('aria-invalid'); extra.removeAttribute('aria-invalid'); roomCount.removeAttribute('aria-invalid');
   if (excluded) { subtotal.textContent='養生費は合計から除外中'; continue; }
   if (!item) { subtotal.textContent='項目を選択してください'; incomplete=true; continue; }
   if (input.value==='') { subtotal.textContent='数量を入力してください'; incomplete=true; continue; }
   if(item.group==='floor' && item.unit==='室' && input.valueAsNumber>4) {
    error.textContent='1室の面積が4㎡を超えるため、㎡単価の床工事を選んでください。';
    input.setAttribute('aria-invalid','true'); subtotal.textContent='施工面積を確認してください'; invalid=true; continue;
   }
   if (!input.validity.valid || !Number.isFinite(input.valueAsNumber)) {
    error.textContent=item.unit==='m'?'数量は0.01〜100,000の範囲で、小数第2位まで入力してください。':'数量は1〜100,000の整数で入力してください。';
    input.setAttribute('aria-invalid','true'); subtotal.textContent='数量を確認してください'; invalid=true; continue;
   }
   if(item.unit==='㎡' && (!extra.validity.valid || !Number.isFinite(extra.valueAsNumber))) {
    error.textContent='その他・追加㎡は0〜100,000の整数で入力してください。';
    extra.setAttribute('aria-invalid','true'); subtotal.textContent='追加面積を確認してください'; invalid=true; continue;
   }
   if(item.group==='floor' && item.unit==='室' && (!roomCount.validity.valid || !Number.isFinite(roomCount.valueAsNumber))) {
    error.textContent='部屋数は1〜100,000の整数で入力してください。'; roomCount.setAttribute('aria-invalid','true'); invalid=true;subtotal.textContent='部屋数を確認してください';continue;
   }
   const quantity=item.group==='floor'&&item.unit==='室'?roomCount.valueAsNumber:input.valueAsNumber+(item.unit==='㎡'?extra.valueAsNumber:0);
   const a=Math.round(item.min*quantity), b=Math.round(item.max*quantity);
   low+=a; high+=b; included++;
   subtotal.textContent=`${item.price} × ${quantity}${item.unit} ＝ ${yen(a)}${a===b?'':' 〜 '+yen(b)}`;
   if(item.group==='floor'&&item.unit==='室') subtotal.textContent+=`（1室あたり${input.valueAsNumber}㎡）`;
   const disposal=disposalFor(item,row,quantity);
   if(disposal) {
    const location=row.querySelector('input[type="text"]').value.trim();
    const label=(location?location+'：':'')+item.name;
    if(disposal.pending) { pendingScope=true; disposalLines.push(label+'：お部屋の広さを選んでください'); }
    else if(disposal.unknown) { unknownWaste=true; disposalLines.push(label+'：この区分の処分費は別途お見積もり'); }
    else {
     const wa=disposal.rate.min*disposal.multiplier,wb=disposal.rate.max*disposal.multiplier;
     wasteLow+=wa; wasteHigh+=wb;
     disposalLines.push(label+' ／ '+disposal.rate.name+' × '+disposal.multiplier+'：'+yen(wa)+(wa===wb?'':' 〜 '+yen(wb)));
    }
   }
  }
  const list=wasteSummary.querySelector('ul'); list.replaceChildren();
  for(const text of disposalLines) { const li=document.createElement('li');li.textContent=text;list.append(li); }
  wasteSummary.querySelector('.calculator-waste-total').textContent=invalid?'数量の入力を確認してください':pendingScope?'お部屋の広さを選ぶと、古い材料の処分費を自動計算します。':included?'産業廃棄物処分費 小計：'+yen(wasteLow)+' 〜 '+yen(wasteHigh)+(unknownWaste?'（別途お見積もり分を除く）':''):'施工内容を選ぶと、対応する処分費をここに表示します。';
  total.textContent=invalid?'数量の入力を確認してください':pendingScope?'お部屋の広さを選んでください':included?`${yen(low+wasteLow)} 〜 ${yen(high+wasteHigh)}${unknownWaste?' ＋ 処分費別途':''}`:'項目と数量を入力してください';
  count.textContent=invalid?'入力を修正すると合計を表示します。':pendingScope?'古い壁紙・床材の処分費を加えるため、お部屋の広さを選んでください。':included?`${included}項目＋自動計算の産業廃棄物処分費${incomplete?'（未入力の行は含んでいません）':''}`:'';
 }
 function addRow(group,focus=true,after=null) {
  if (group==='protection') protection.checked=true;
  const id=++serial;
  const row=document.createElement('fieldset'); row.className='calculator-row'; row.dataset.group=group;
  row.innerHTML=`<legend>${groups[group]}</legend><div class="calculator-row-grid"><label for="calc-item-${id}">施工内容・項目<select id="calc-item-${id}"><option value="">項目を選択してください</option></select></label><label for="calc-quantity-${id}">数量 <span class="calculator-unit"></span><input id="calc-quantity-${id}" type="number" inputmode="decimal" min="1" max="100000" step="1" aria-describedby="calc-error-${id}"></label><button type="button" class="calculator-remove" aria-label="${groups[group]}の行を削除">削除</button></div><p class="calculator-item-note"></p><p class="calculator-error" id="calc-error-${id}"></p><p class="calculator-subtotal"></p>`;
  const location=document.createElement('label'); location.className='calculator-location';
  location.textContent='部屋・施工箇所（任意）';
  const locationInput=document.createElement('input'); locationInput.type='text'; locationInput.maxLength=80;
  locationInput.placeholder=group==='waste'?'例：リビングのクロス撤去分':'例：リビング・寝室・アクセント壁';
  location.append(locationInput); row.querySelector('.calculator-row-grid').before(location);
  const select=row.querySelector('select'),input=row.querySelector('input[type="number"]');
  input.classList.add('calculator-quantity');
  const extraLabel=document.createElement('label'); extraLabel.className='calculator-extra-label'; extraLabel.hidden=true;
  extraLabel.textContent='その他・追加㎡（特殊な場所の面積）';
  const extra=document.createElement('input'); extra.type='number'; extra.className='calculator-extra-area'; extra.min='0'; extra.max='100000'; extra.step='1'; extra.value='0'; extra.inputMode='numeric'; extra.setAttribute('aria-describedby',`calc-error-${id}`);
  extraLabel.append(extra);
  const extraNote=document.createElement('span'); extraNote.className='calculator-extra-note'; extraNote.textContent='同じ材料・単価で施工する追加部分の面積です。上の施工面積に加えて計算します。'; extraLabel.append(extraNote);
  row.querySelector('.calculator-row-grid').after(extraLabel);
  const roomLabel=document.createElement('label'); roomLabel.className='calculator-room-label';roomLabel.hidden=true;roomLabel.textContent='部屋数（室）';
  const roomCount=document.createElement('input');roomCount.type='number';roomCount.className='calculator-room-count';roomCount.min='1';roomCount.max='100000';roomCount.step='1';roomCount.value='1';roomCount.inputMode='numeric';roomCount.setAttribute('aria-describedby',`calc-error-${id}`);roomLabel.append(roomCount);extraLabel.after(roomLabel);
  roomCount.addEventListener('input',calculate);
  const conversionNote=document.createElement('p');conversionNote.className='calculator-conversion-note';conversionNote.setAttribute('role','status');row.querySelector('.calculator-item-note').after(conversionNote);
  const scopeLabel=document.createElement('label'); scopeLabel.className='calculator-scope-label'; scopeLabel.hidden=true;
  scopeLabel.textContent='お部屋の広さを教えてください';
  const scope=document.createElement('select'); scope.className='calculator-scope'; scopeLabel.append(scope); extraLabel.after(scopeLabel);
  const scopeHelp=document.createElement('span');scopeHelp.className='calculator-extra-note';scopeHelp.textContent='古い壁紙・床材の処分費を計算するために選びます。工事費とは別に計算して、合計に加えます。';scopeLabel.append(scopeHelp);
  scope.addEventListener('change',calculate);
  function updateScope(item) {
   const previous=scope.value; scope.replaceChildren();
   const index=items.filter(i=>i.group===item?.group).indexOf(item);
   scopeLabel.hidden=!item||!['wall','floor'].includes(item.group)||(item.group==='wall'&&index===4);
   let options=[];
   if(!scopeLabel.hidden) {
    if(item.group==='wall'&&index===2) options=[['new','新規施工（新築・ボード面）']];
    else if(item.group==='wall') options=[['','お部屋の広さを選んでください'],['small','トイレ・洗面所・壁1面だけの貼替え'],['room','6〜8畳のお部屋（壁・天井）'],['ldk','15〜20畳のリビング・ダイニングなど'],['other','上記以外のお部屋（処分費は個別にご案内）']];
    else if(item.unit==='室') options=[['small','トイレ・洗面所（〜4㎡）／入力した室数分']];
    else if(item.unit==='m') options=[['skirting','ソフト巾木（1部屋分）']];
    else options=[['','お部屋の広さを選んでください'],['small','トイレ・洗面所（〜4㎡）'],['room','6畳間（約10㎡）'],['other','上記以外のお部屋（処分費は個別にご案内）']];
   }
   for(const [value,text] of options) { const option=document.createElement('option'); option.value=value;option.textContent=text;scope.append(option); }
   if(options.some(([value])=>value===previous)) scope.value=previous;
  }
  for(const item of items.filter(i=>i.group===group)) {
   const option=document.createElement('option'); option.value=item.id; option.textContent=item.name+'（'+item.price+'）'; select.append(option);
  }
  select.addEventListener('change',()=>{
   const item=items.find(i=>i.id===select.value);
   const decimal=item&&item.unit==='m';
   const packageRoom=item?.group==='floor'&&item.unit==='室';
   input.min=decimal?'0.01':'1'; input.max=packageRoom?'4':'100000';input.step=decimal?'0.01':'1'; input.inputMode=decimal?'decimal':'numeric';
   row.querySelector('.calculator-unit').parentElement.firstChild.textContent=packageRoom?'施工面積（1室あたり） ':item?.unit==='㎡'?'施工面積 ':item?.unit==='m'?'施工延長 ':'数量 ';
   row.querySelector('.calculator-unit').textContent=item?'（'+(packageRoom?'㎡・4㎡まで':item.unit)+'）':'';
   roomLabel.hidden=!packageRoom;
   conversionNote.textContent='';
   row.querySelector('.calculator-item-note').textContent=item?.note||'';
   extraLabel.hidden=item?.unit!=='㎡';
   if(item?.unit!=='㎡') extra.value='0';
   updateScope(item);
   if(item&&input.value==='') input.value='1';
   calculate();
  });
  input.addEventListener('input',()=>{
   const item=items.find(i=>i.id===select.value);
   if(item?.group==='floor'&&item.unit==='室'&&input.valueAsNumber>4&&roomCount.validity.valid) {
    const floorItems=items.filter(i=>i.group==='floor');
    const areaRate=floorItems[floorItems.indexOf(item)+1];
    const area=input.valueAsNumber*roomCount.valueAsNumber;
    select.value=areaRate.id; select.dispatchEvent(new Event('change'));
    input.value=String(area);roomCount.value='1';scope.value='other';
    conversionNote.textContent='4㎡を超えたため、室単位の料金から㎡単価へ切り替えました。お部屋の広さもご確認ください。料金表にない規模の処分費は別途お見積もりです。';
   }
   calculate();
  });
  extra.addEventListener('input',calculate);
  locationInput.addEventListener('input',calculate);
  row.querySelector('.calculator-remove').addEventListener('click',()=>{
   const next=row.nextElementSibling||row.previousElementSibling;
   row.remove(); calculate();
   (next?.querySelector('select')||root.querySelector('[data-add]')).focus();
  });
  const repeat=document.createElement('button'); repeat.type='button'; repeat.className='calculator-repeat';
  repeat.textContent=group==='waste'?'＋ 産業廃棄物処分費の入力欄を追加':group==='wall'?'＋ クロスの部屋・アクセント箇所を追加':group==='floor'?'＋ CF・床の部屋・箇所を追加':'＋ 養生する場所を追加';
  repeat.addEventListener('click',()=>addRow(group,true,row)); row.append(repeat);
  if(after) after.after(row); else rows.append(row);
  calculate(); if(focus) select.focus();
 }
 root.querySelectorAll('[data-add]').forEach(button=>button.addEventListener('click',()=>addRow(button.dataset.add)));
 protection.addEventListener('change',calculate);
 form.addEventListener('submit',event=>event.preventDefault());
 form.addEventListener('reset',event=>{
  event.preventDefault(); rows.replaceChildren(); protection.checked=true; initialRows(); rows.querySelector('select').focus();
 });
 root.querySelector('.calculator-interactive').hidden=false;
 function initialRows() { ['wall','floor'].forEach(group=>addRow(group,false)); }
 initialRows();
})();
