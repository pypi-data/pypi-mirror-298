/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/



class _IdeEditorHandler extends TerminalRunner {

  constructor(editorId){
    super(editorId)
    this.termId        = "term_" + editorId
    this.commentIdH    = "#comment_" + editorId
    this.globalIdH     = "#global_" + editorId
    this.inputIdH      = "#input_" + editorId
    this.counterH      = "#compteur_" + editorId
    this.delay         = 200
    this.editor        = null
    this.resizedTerm   = !this.isVert
    this.getCodeToTest = ()=>this.editor.getSession().getValue()
    this._init()
  }

  _init(){
    this.hiddenDivContent = true
  }



  // @Override
  build(){
    const ideThis = this

    this.setupAceEditor()   // Create and define this.editor

    // Bind the ### "button":
    $(this.commentIdH).on("click", this.toggleComments.bind(this))

    const ideLoader = txt => {
      this.applyCodeToEditorAndSave(txt)
      this.focusEditor()
    }

    // Bind all buttons below the IDE
    $(this.globalIdH).find("button").each(function(){
      const btn  = $(this)
      const kind = btn.attr('btn_kind')
      let callback
      switch(kind){
        case 'play':      callback = ideThis.playFactory() ; break
        case 'check':     callback = ideThis.validateFactory() ; break

        case 'download':  callback = _=>ideThis.download() ; break
        case 'upload':    callback = _=>uploader(ideLoader) ; break

        case 'restart':   callback = _=>ideThis.restart() ; break
        case 'save':      callback = _=>{ideThis.save(); ideThis.focusEditor()} ; break

        case 'corr_btn':  if(!CONFIG.inServe) return;
                          callback = ideThis.validateCorrFactory() ; break
        case 'show':      if(!CONFIG.inServe) return;
                          callback = ideThis.revealSolutionAndRems.bind(ideThis) ; break

        default: throw new Error(`Y'should never get there, mate... (${ kind })`)
      }
      btn.on('click', callback)
    })


    // Build the related terminal and add the resize listener (because of the intermediate div
    // wrappers, IDE's terminal will not resize automatically):
    super.build(this.termId)
    window.addEventListener(
      'resize',
      _.throttle( this.terminalAutoWidthOnResize.bind(this), 50, {leading:false, trailing:true} )
    )


    // Then extract its current height and enforce the value on the terminal if isVert is true.
    // This has to be done on "next tick" and after creation of the terminal instance, so that
    // the editor height has been actually applied.
    if(this.isVert){

      // Resize on next tick, once the editor has been filled with code (automatic height):
      setTimeout(_=>this.resizeVerticalTerm(false))

      // In case an IDEv is "tabbed", it won't scale properly because the editor is not handled
      // the same way, so put in place a "run once" click event, to resize it when the user
      // clicks on the _parent_ div (because the terminal itself is 0px high! XD )
      this.addEventToRunOnce(this.terminal.parent(), _=>this.resizeVerticalTerm())
    }
  }




  resizeVerticalTerm(mark=true){
    if(!this.isVert || this.resizedTerm) return;
    jsLogger("[CheckPoint] - Handle terminal window size")

    const divHeight = $('#'+this.id).css('height')
    const term_div = $(`${ this.globalIdH } .term_editor_v`)
    term_div.css("height", divHeight)
    this.resizedTerm = mark
  }



  /**Create and setup the ACE editor for the current Ide instance.
   * */
  setupAceEditor() {

    // https://github.com/ajaxorg/ace/blob/092b70c9e35f1b7aeb927925d89cb0264480d409/lib/ace/autocomplete.js#L545
    const options = {
        autoScrollEditorIntoView: false,
        copyWithEmptySelection:   true,               // active alt+flèches pour déplacer une ligne, aussi
        enableBasicAutocompletion:true,
        enableLiveAutocompletion: false,
        enableSnippets:           true,
        tabSize:                  4,
        useSoftTabs:              true,               // Spaces instead of tabs
        navigateWithinSoftTabs:   false,              // this is _fucking_ actually "Atomic Soft Tabs"...
        printMargin:              false,              // hide ugly margins...
        maxLines:                 this.maxIdeLines,
        minLines:                 this.minIdeLines,
        mode:                     "ace/mode/python",
        theme:                    getTheme(),
    }

    const editor = this.editor = ace.edit(this.id, options);
    if(CONFIG._devMode) CONFIG.editors[this.id] = editor

    editor.commands.bindKey(
        { win: "Ctrl-Space", mac: "Cmd-Space" }, "startAutocomplete"
    )
    editor.commands.addCommand({
        name: "commentTests",
        bindKey: { win: "Ctrl-I", mac: "Cmd-I" },
        exec: this.toggleComments.bind(this),
    })
    editor.commands.addCommand({
        name: "runPublicTests",
        bindKey: { win: "Ctrl-S", mac: "Cmd-S" },
        exec: this.playFactory(),
    })
    if(this.hasCheckBtn){
        editor.commands.addCommand({
        name: "runValidationTests",
        bindKey: { win: "Ctrl-Enter", mac: "Cmd-Enter" },
        exec: this.validateFactory(),
      })
    }

    // Content of the editor is saved every `CONFIG.ideKeyStrokesSave` keystrokes:
    let nChange = 0;
    this.editor.addEventListener("input", _=>{
        if(nChange++ >= CONFIG.ideKeyStrokesSave){
          nChange=0
          this.save()
        }
    })

    // Try to restore a previous session, or extract default starting code:
    let exerciseCode = this.getStartCode(true)
    this.applyCodeToEditorAndSave(exerciseCode)
    this.editor.resize();
  }



  // @Override
  getTerminalBindings(){

    // Ensure the focus is given back to the terminal after an action triggered from it!
    const asyncTermFocus=(cbk)=>async e=>{
      await cbk(e)
      this.editor.blur()
      this.terminal.focus()
    }
    return ({
      ...super.getTerminalBindings(),
      'CTRL+I': asyncTermFocus(this.toggleComments.bind(this)),
      'CTRL+S': asyncTermFocus(this.playFactory()),
      ...(!this.hasCheckBtn ? {} : {'CTRL+ENTER': asyncTermFocus(this.validateFactory())} ),
    })
  }



  /**Automatically gives the focus to the ACE editor with the given id.
   * */
  focusEditor(){
    this.editor.focus()
  }


  /**Add the `tests` section to the given code, joining them with the appropriated
   * string/comment if needed.
   * */
  _joinCodeAndPublicSections(userCode){
    const editorCode = [
      userCode,
      this.publicTests
    ].filter(Boolean)
     .join(CONFIG.lang.tests.msg)
    return editorCode
  }



  /**Build (or extract if allowed) the initial code to put in the editor.
   * */
  getStartCode(attemptLocalStorageExtraction=false){
    let exerciseCode = ""

    if(attemptLocalStorageExtraction){
      exerciseCode = localStorage.getItem(this.id) || ""
    }
    if(!exerciseCode){
      exerciseCode = this._joinCodeAndPublicSections(this.userContent)
    }

    // Enforce at least one empty line of code in the editor, so that the terminal prompt
    // is always visible for IDEv:
    exerciseCode = exerciseCode.replace(/\n+$/,'')
    if(!exerciseCode) exerciseCode = '\n'

    return exerciseCode+"\n"
  }


  /**Takes in the id string of an editor, or an ACE editor as first argument, and the
   * code string to apply to it, and:
   *      - set the editor content to that string
   *      - save the code to the localStorage
   * */
  applyCodeToEditorAndSave(exerciseCode){
    exerciseCode ||= ""
    this.editor.getSession().setValue(exerciseCode);
    this.save(exerciseCode)
  }



  //-------------------------------------------------------------------------



  /**Extract the current content of the given editor, explore it, and toggle all the LOCs
   * found after the `TestToken` token.
   *
   * Rules for toggling or not are:
   *      - leading spaces do not affect the logic.
   *      - comment out if the first non space character is not "#".
   *      - if the first non space char is "#" and there is no spaces after it, uncomment.
   * */
  toggleComments(e) {
    if(e && e.preventDefault) e.preventDefault()

    const codeLines   = this.getCodeToTest().split('\n')
    const pattern     = CONFIG.lang.tests.as_pattern
    const iTestsToken = codeLines.findIndex(s=>pattern.test(s))

    /// No tests found:
    if(iTestsToken<0) return;

    const toggled = codeLines.slice(iTestsToken+1).map(s=>{
        return s.replace(CONFIG.COMMENTED_PATTERN, (_,spaces,head,tail)=>{
            if(head=='#' && tail!=' ') return spaces+tail
            if(head!='#') return spaces+'#'+head+tail
            return _
        })
    })
    codeLines.splice(iTestsToken+1, toggled.length, ...toggled)
    const repl = codeLines.join('\n')
    this.applyCodeToEditorAndSave(repl)
    this.focusEditor()
  }



  /**Download the current content of the editor to the download folder of the user.
   * */
  download(){   jsLogger("[Download]")

    let ideContent = this.getCodeToTest() + "" // enforce stringification in any case
    downloader(ideContent, this.pyName)
    this.focusEditor()
  }


  /**Reset the content of the editor to its initial content, and reset the localStorage for
   * this editor on the way.
   * */
  restart(){    jsLogger("[Restart]")

    const exerciseCode = this.getStartCode()
    this.applyCodeToEditorAndSave(exerciseCode)
    this.focusEditor()
  }



  /**Save the current IDE content of the user, or the given code, into the localStorage
  * of the navigator.
  * */
  save(givenCode=""){   jsLogger("[Save]")
    const currentCode = givenCode || this.getCodeToTest()
    localStorage.setItem(this.id, currentCode);
  }

  playFactory(){  throw new Error("Should be overridden in child class") }
  validateFactory(){ throw new Error("Should be overridden in child class") }

  /**Is the current action "running the public tests"?
   * */
  isPlaying(){  return this.running.includes(CONFIG.running.play) }

  /**Is the current action "running the validation tests"?
   * */
  isChecking(){ return this.running.includes(CONFIG.running.validate) }
}


















class IdeRunner extends _IdeEditorHandler {



  // @Override
  build(){
    super.build()
    if(this.profile=='revealed'){
      this.revealSolutionAndRems(true)
    }
  }


  /**Does nothing, but catch any call on the parent class, which would raise an error
   * because prefillTerm is undefined, for IDEs.
   * */
  prefillTermIfAny(){}



  /**The terminal behaves differently when IDE content is run, so must be handled from here.
   * (mostly: through command lines, the terminal content is not cleared).
   *
   *  - If not paused, the terminal automatically displays a new line for a fresh command.
   *  - So clear content only after if got paused.
   *  - Then show to the user that executions started and enforce terminal GUI refresh,
   *    with a tiny pause so that the user has time to see the "cleared" terminal content.
   *  - Then, relay to super setup methods.
   * */
  async setupRuntimeIDE() {
    jsLogger("[CheckPoint] - setupRuntimeIDE IdeRunner")

    this.resizeVerticalTerm()           // needed in case the first click is on a button
    this.terminalAutoWidthOnResize()

    // save before anything else, in case an error occur somewhere...
    const editorCode = this.getCodeToTest()
    this.save(editorCode)
    this.storeUserCodeInPython('__USER_CODE__', editorCode)

    this.terminal.pause()           // Deactivate user actions in the terminal until resumed
    this.terminal.clear()           // To do AFTER pausing...
    this.terminalDisplayOnStart()   // Handle the terminal display for the current action
    await sleep(this.delay)         // Terminal "blink", so that the user always sees a change

    return this.setupRuntime()
  }


  /**Things to display in the terminal at the very beginning of the executions.
   * */
  terminalDisplayOnStart(){
    this.terminalEcho(CONFIG.lang.runScript.msg)
  }



  async teardownRuntimeIDE(runtime) {
    jsLogger("[CheckPoint] - IdeRunner teardownRuntime")

    // Restore default state first, in case a validation occurred (=> restore stdout behaviors!)
    runtime.refreshStateWith()

    // Handle any extra final message (related to revelation of solutions & REMs)
    if(runtime.finalMsg) this.giveFeedback(runtime.finalMsg)

    await this.teardownRuntime(runtime)
    this.storeUserCodeInPython('__USER_CODE__', "")
  }



  /**If the current action has been successful until now, display the appropriate
   * message in the terminal.
   * */
  codeSnippetEndFeedback(runtime, step){
    if(runtime.stopped || !step) return

    const playing = this.isPlaying()
    const intro   = playing ? "" : CONFIG.lang.validation.msg
    const section = CONFIG.lang[step].msg
    const ok      = CONFIG.lang.successMsg.msg

    let msg = `${ intro }${ section }: ${ ok }`
    if(playing && !this.hasCheckBtn && !this.publicTests){    // TODO: why "&& !this.publicTests"...? Seems useless :thinking:
      msg = CONFIG.lang.successMsgNoTests.msg
    }

    this.terminalEcho(msg)

    // If no error yet and secret tests exist while running the public tests right now,
    // prepare a "very final" message reminding to try the validations:
    if(playing && this.hasCheckBtn){
      runtime.finalMsg = CONFIG.lang.unforgettable.msg
    }
  }





  //--------------------------------------------------------------------




  /**Build the public tests runner routine.
   * */
  playFactory(runningMan=CONFIG.running.play){
    return this.lockedRunnerWithBigFailWarningFactory(
      runningMan,
      this.setupRuntimeIDE,
      this.playThroughRunner,
      this.teardownRuntimeIDE,
    )
  }

  /**Build the validation tests runner routine.
   * */
  validateFactory(runningMan=CONFIG.running.validate){
    return this.lockedRunnerWithBigFailWarningFactory(
      runningMan,
      this.setupRuntimeIDE,
      this.validateThroughRunner,
      this.teardownRuntimeIDE,
    )
  }

  /**Build the correction validation runner routine.
   * NOTE: the pyodideLock setup is not correct here (swaps done outside of it), but it shouldn't
   *       ever cause troubles, as long as this method is not used in the IdeTester objects.
   * */
  validateCorrFactory(){
    const cbk = this.validateFactory()
    const wrapper = async (e)=>{
      jsLogger("[CheckPoint] - corr_btn start")

      const codeGetter   = this.getCodeToTest
      const currentEditor= this.getCodeToTest()
      const profile      = this.profile
      this.getCodeToTest = ()=>this.corrContent
      this.data.profile  = null    // REMINDER: getters without setters!

      let out
      try{
        out = await cbk(e)
      }finally{
        jsLogger("[CheckPoint] - corr_btn validation done")
        this.data.profile  = profile
        this.getCodeToTest = codeGetter
        this.save(currentEditor)    // Ensure the corr content doesn't stay stored in localStorage
      }
      return out
    }
    return wrapper
  }




  //--------------------------------------------------------------------




  /** `lockedRunnerWithBigFailWarningFactory(@action)` routine, to run public tests.
   * */
  async playThroughRunner(runtime){
    const code = this.getCodeToTest()
    const step = CONFIG.section.editor
    await this.runPythonCodeWithOptionsIfNoStdErr(code, runtime, step)
  }


  /** `lockedRunnerWithBigFailWarningFactory(@action)` routine, to run validation tests.
   * */
  async validateThroughRunner(runtime){

    // env section is behaving like the editor one (should be changed...?)
    let decrease_count = this.canDecreaseAttempts(CONFIG.section.editor)

    // If an error already occurred, stop everything...
    if(runtime.stopped){

      // ... but decrease the number attempts and run teardown if this was AssertionError.
      if(runtime.isAssertErr){
        this.handleRunOutcome(runtime, decrease_count)
      }

    }else{

      const validation_state = {
        autoLogAssert:    this.autoLogAssert,
        purgeStackTrace:  this.showOnlyAssertionErrorsForSecrets,
        withStdOut:      !this.deactivateStdoutForSecrets,
      }
      const toRun = [
        [this.getCodeToTest(), CONFIG.section.editor,  {}],
        [this.publicTests,     CONFIG.section.public,  validation_state],
        [this.secretTests,     CONFIG.section.secrets, validation_state],
      ]

      for(const [code, testSection, state] of toRun){
        jsLogger("[CheckPoint] - Run validation step:", testSection)

        runtime.refreshStateWith(state)
        await this.runPythonCodeWithOptionsIfNoStdErr(code, runtime, testSection)
        if(runtime.stopped){
          decrease_count = this.canDecreaseAttempts(testSection)
          break
        }
      }

      // Reveal solution and REMs on success, or if the counter reached 0 and the sol&REMs content
      // is still hidden, then prepare an appropriate revelation message if needed (`finalMsg`).
      this.handleRunOutcome(runtime, decrease_count)
    }
  }


  /**Return true if the current section allow to decrease the number of attempts,
   * during a validation
   * */
  canDecreaseAttempts(testSection){
    const wanted      = CONFIG.section[ this.decreaseAttemptsOnUserCodeFailure ]
    const allowedFrom = CONFIG.sectionOrder[ wanted ]
    const currentAt   = CONFIG.sectionOrder[ testSection ]
    const canDecrease = currentAt >= allowedFrom
    return canDecrease
  }





  //-----------------------------------------------------------------------





  /**Reveal solution and REMs on success, or if the counter reached 0 and the sol&REMs content
   * is still hidden, then prepare an appropriate revelation message if needed (`finalMsg`).
   *
   * Do not forget that any error related feedback has already been printed to the console, so
   * when it comes to feedback given in this method, it's only about a potential "final message".
   * */
  handleRunOutcome(runtime, allowCountDecrease){
    const success    = !runtime.stopped
    const revealable = this.corrRemsMask && this.hiddenDivContent && !this.profile

    jsLogger("[CheckPoint] - handleRunOutcome")
    // console.log("[OutCome]", JSON.stringify({ success, pof:this.profile, revealable, hidden:this.hiddenDivContent, allowCountDecrease: !!allowCountDecrease, mask:this.corrRemsMask, N:this.attemptsLeft}))

    if(!success){
      runtime.finalMsg = ""         // Reset any default message "terminé sans erreurs" (TOTO: became useless?)
      if(allowCountDecrease){
        this.decreaseIdeCounter()
      }
    }

    if( revealable && (success || this.attemptsLeft==0) ){
      jsLogger("[OutCome]", 'reveal!', success)
      runtime.finalMsg = success ? this._buildSuccessMessage(revealable)
                                 : this._getSolRemTxt(false)
      this.revealSolutionAndRems()

    }else if(success && !revealable && this.corrRemsMask && this.hiddenDivContent){
      runtime.finalMsg = this._buildSuccessMessage(revealable)
    }
  }


  /**Decrease the number of attempts left, EXCEPT when:
   *    - the solution is already revealed,
   *    - the number of attempts is infinite,
   *    - there are no attempts left (redundant with revelation condition, but hey...).
   */
  decreaseIdeCounter(){
    jsLogger("[CheckPoint] - decreaseIdeCounter")
    if(!this.hiddenDivContent) return    // already revealed => nothing to change.

    // Allow going below 0 so that triggers once only for failure.
    const nAttempts = Math.max(-1, this.attemptsLeft - 1)
    this.data.attempts_left = nAttempts

    // Update the GUI counter if needed (check for encryption in case
    // the user already solved the problem)
    if (Number.isFinite(nAttempts) && nAttempts >= 0){
      this.setAttemptsCounter(nAttempts)
    }
  }


  setAttemptsCounter(nAttempts){
    $(this.counterH).text(nAttempts)
  }


  /**Reveal corr and/or REMs (visible or not) contents.
   * When reaching this method, it is already sure by contract, that the revelation must occur.
   * The only piece of contract this method is holding is that if flags the revelation as done,
   * and it decides if the div content has to be decompressed or not on the way.
   * */
  revealSolutionAndRems(skipMathJax=false){
    jsLogger("[CheckPoint] - Enter revealSolutionAndRems")
    const sol_div = $("#solution_" + this.id)

    // Need to check here one more time against hiddenDivContent because of the show button logic.
    if(this.hiddenDivContent && this.isEncrypted){
      jsLogger("[CheckPoint] - revealed!")

      const compressed = sol_div.text()
      const content = decompressLZW(compressed, "ides.encrypt_corrections_and_rems")
      sol_div.html(content)
      this.hiddenDivContent = false   // Forbid coming back here (last in case of errors...)
    }
    sol_div.attr('class', '')         // Unhide
    if(!skipMathJax) mathJaxUpdate()  // Enforce formatting, if ever...
  }



  _buildSuccessMessage(revealable){
    const emo = choice(CONFIG.MSG.successEmojis)
    const moreInfo = !revealable ? '' : this._getSolRemTxt(true)
    return `${ CONFIG.lang.successHead.msg } ${ emo } ${ CONFIG.lang.successHeadExtra.msg }${ moreInfo }`
  }


  _getSolRemTxt(isSuccess){
    if(!this.corrRemsMask) return ""

    const hasCorr  = this.corrRemsMask & 1
    const hasRems  = this.corrRemsMask & 2
    const hasBoth  = this.corrRemsMask == 3
    const msg      = []
    const sentence = []

    const pushSentence = (prop, kind='msg') => sentence.push(CONFIG.lang[prop][kind])

    msg.push(
      isSuccess ? "\n"+CONFIG.lang.successTail.msg
                : CONFIG.lang.failHead.msg
    )

    if(hasCorr) pushSentence('revealCorr')
    if(hasBoth) pushSentence('revealJoin')
    if(hasRems) pushSentence('revealRem')

    if(!isSuccess){
        if(sentence.length) sentence[0] = _.capitalize(sentence[0])

        if(hasBoth) pushSentence('failTail', 'plural')
        else        pushSentence('failTail')
    }
    msg.push(...sentence)
    const output = msg.join(' ').trimEnd() + "."

    // console.log("[OutComeSolRemTxt]", JSON.stringify({isSuccess, msg, mask:this.corrRemsMask, sentence, output}))
    return output
  }
}

CONFIG.CLASSES_POOL.Ide = IdeRunner
