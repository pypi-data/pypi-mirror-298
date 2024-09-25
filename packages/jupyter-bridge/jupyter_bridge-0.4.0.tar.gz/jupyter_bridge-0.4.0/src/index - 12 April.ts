// Import necessary dependencies from React, JupyterLab, and other modules
import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { INotebookTracker, NotebookPanel, NotebookActions } from '@jupyterlab/notebook';
import { ICellFooter, Cell } from '@jupyterlab/cells';
import { ReadonlyPartialJSONObject } from '@lumino/coreutils';
import { CommandRegistry } from '@lumino/commands';
import { IEditorServices } from '@jupyterlab/codeeditor';
import { OutputArea, OutputAreaModel } from '@jupyterlab/outputarea';
import { RenderMimeRegistry } from '@jupyterlab/rendermime';


import '../style/index.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

// Define CSS classes used in the cell footer.
const CSS_CLASSES = {
  CELL_FOOTER: 'jp-CellFooter',
  CELL_FOOTER_DIV: 'ct-cellFooterContainer',
  CELL_FOOTER_BUTTON: 'ct-cellFooterBtn',
  CELL_TOGGLE_BUTTON: '.ct-toggleBtn',
  CUSTOM_OUTPUT_AREA: 'custom-output-area', 
};

// Define command constants
const COMMANDS = {
  HIDE_CELL_CODE: 'hide-cell-code',
  SHOW_CELL_CODE: 'show-cell-code',
  RUN_SELECTED_CODECELL: 'run-selected-codecell',
  CLEAR_SELECTED_OUTPUT: 'clear-output-cell',
  TOGGLE_EXPL_CELL: '',
};

// Function to activate custom commands
function activateCommands(app: JupyterFrontEnd, tracker: INotebookTracker): Promise<void> {
  // Output a message to the console to indicate activation
  console.log('JupyterLab extension is activated!');

  // Wait for the app to be restored before proceeding
  Promise.all([app.restored]).then(([params]) => {
    const { commands, shell } = app;

    // Function to get the current NotebookPanel
    function getCurrent(args: ReadonlyPartialJSONObject): NotebookPanel | null {
      const widget = tracker.currentWidget;
      const activate = args.activate !== false;

      if (activate && widget) {
        shell.activateById(widget.id);
      }

      return widget;
    }

    /**
    * Function to check if the command should be enabled.
    * It checks if there is a current notebook widget and if it matches the app's current widget.
    * If both conditions are met, the command is considered enabled.
    */
    function isEnabled(): boolean {
      return (
        tracker.currentWidget !== null &&
        tracker.currentWidget === app.shell.currentWidget
      );
    }

    // Define a command to toggle the visibility of the explanatory markdown cell
    commands.addCommand(COMMANDS.TOGGLE_EXPL_CELL, {
      label: 'Toggle Explanatory Cell',
      execute: () => {
        const notebookPanel = tracker.currentWidget;
        if (!notebookPanel) return; // Exit if no notebook is focused

        const cells = notebookPanel.content.widgets;
        const activeCellIndex = cells.findIndex(cell => notebookPanel.content.isSelectedOrActive(cell));

        if (activeCellIndex > 0) { // Ensure there is a preceding cell
          const precedingCell = cells[activeCellIndex - 1];
          if (precedingCell.model.type === 'markdown') {
            // Check if the preceding markdown cell is marked as "explanatory"
            const isExplanatory = precedingCell.model.getMetadata('explanatory') === true;
            if (isExplanatory) {
              //Apply the class hidden to set the display to none
              precedingCell.toggleClass('hidden');
            }
          }
        }
      },
      isEnabled
    });
    
    // Define a command to hide the code in the current cell
    commands.addCommand(COMMANDS.HIDE_CELL_CODE, {
      label:'Hide Cell',
      execute: args => {
        const current = getCurrent(args);
        if (current) {
          const { content } = current;
          NotebookActions.hideCode(content);
        }
      },
      isEnabled
    });

    // Define a command to show the code in the current cell
    commands.addCommand(COMMANDS.SHOW_CELL_CODE , {
      label: 'Show Cell',
      execute: args => {
        const current = getCurrent(args);
        if (current) {
          const { content } = current;
          NotebookActions.showCode(content);
        }
      },
      isEnabled
    });

    // Define a command to run the code in the current cell
    commands.addCommand(COMMANDS.RUN_SELECTED_CODECELL, {
      label: 'Run Cell',
      execute: args => {
        const current = getCurrent(args);
        if (current) {
          const { context, content } = current;
          NotebookActions.run(content, context.sessionContext);          
        }
      },
      isEnabled
    });

    commands.addCommand(COMMANDS.CLEAR_SELECTED_OUTPUT, {
      label: 'Clear Output',
      execute: args => {
        const current = getCurrent(args);
        if (current) {
          const { content } = current;
          NotebookActions.clearOutputs(content);
        }
      },
      isEnabled
    });
  });

  // Add a listener to handle when notebooks are loaded or when new cells are added to them
  tracker.widgetAdded.connect((sender, notebookPanel) => {
    // Add a listener for when the content of any cell in the notebook changes
    const model = notebookPanel.content.model;
    if(model === null) return; 

    notebookPanel.content.model?.cells.changed.connect((sender, change) => {
      if (change.type === 'add' || change.type === 'set') {
        change.newValues.forEach((cellModel) => {
          if (cellModel.type === 'markdown') {
            // Directly using cellModel to access and modify the cell's content and metadata
            let cellText: string = cellModel.toJSON().source as string;
            const firstLine = cellText.split('\n')[0].trim();
  
            if (firstLine.includes('#explanatory')) {
              // Mark the cell as explanatory
              cellModel.setMetadata('explanatory', true);
              // Remove the #explanatory marker from the cell text
              // Not working...
              cellText = cellText.replace('#explanatory', '').trim();
              console.log('Remove explanatory marker and cellText value: ' + cellText)
              cellModel.toJSON().source = cellText; // Directly update the cell's text
            } else if (firstLine.includes('#notexplanatory')) {
              cellModel.deleteMetadata('explanatory');
              // Remove the #notexplanatory marker from the cell text
              // Not working...
              cellText = cellText.replace('#notexplanatory', '').trim();
              cellModel.toJSON().source = cellText; // Directly update the cell's text
            }
          }
        });
      }
    });
  });

  //Event listener to collapse code cells when a notebook is loaded
  tracker.widgetAdded.connect((sender, panel) => {
    console.log('Notebook widget added');

    function collapseAllCodeCells(panel: NotebookPanel) {
      const { content } = panel;
      content.widgets.forEach(cell => {
          if (cell.model.type === 'code') {
              NotebookActions.hideAllCode(content);
          }
      });
    }
    
    // Function to handle initial setup to flag explanatory cells and their related code cells
    function setupCellFlags(panel: NotebookPanel): void {
      let codeCellCounter = 0; //debugging counter

      //First pass: set "has_explanation' to false for all code cells
      panel.content.widgets.forEach((cell, index) => {
        // Ensure every code cell has 'has_explanation' set to false initially
        if (cell.model.type === 'code') {     
          cell.addClass('ct-code-cell');     
          cell.model.setMetadata('has_explanation', false);
        }
      });
      
      let previousCellIsExplanatory = false;
      
      // Second pass: Check each cell and update "has_explanation" based on the previous cell's "explanatory" status
      panel.content.widgets.forEach((cell, index) => {        
        if (cell.model.type === 'markdown') {
          const isExplanatory = cell.model.getMetadata('explanatory') === true;
          if (isExplanatory) {
            cell.addClass('ct-explanatory-cell');
            cell.addClass('hidden');
          }
          previousCellIsExplanatory = isExplanatory;
        } else if (cell.model.type === 'code') {
          codeCellCounter++; //Increment for each code cell encountered
          if (previousCellIsExplanatory) {
            console.log('Entering code cell {codeCellCounter} after an explanatory cell');
            cell.model.setMetadata('has_explanation', true);            
            previousCellIsExplanatory = false;
          } else {
            console.log(`Entering code cell ${codeCellCounter} with no preceding explanatory cell`);
          }
          previousCellIsExplanatory = false; //Reset flag
        } else {
          //Reset flag for non-code, non-markdown cells if any
          console.log('None code, non markdown')
          previousCellIsExplanatory = false;
        }
      });
      
      console.log('Completed setting has_explanation flags.');
    }
    
    // Collapse code cells when the current notebook is loaded
    panel.context.ready.then(() => {
      console.log('Notebook context is ready');

      collapseAllCodeCells(panel);  
      setupCellFlags(panel);      

      // Additional debugging: Log the metadata of all cells
      console.log('Logging cell metadata after setup...');
      panel.content.widgets.forEach((cell, index) => {
          console.log(`Cell ${index} (${cell.model.type}) metadata:`, cell.model.metadata as any);
      });
    });
  });

  return Promise.resolve();
}

/**
 * Extend the default implementation of an `IContentFactory`.
 */
class ContentFactoryWithFooterButton extends NotebookPanel.ContentFactory {
  commands: CommandRegistry;

  constructor(commands: CommandRegistry, options: Cell.ContentFactory.IOptions) {
    super(options); // Pass options to the superclass constructor
    this.commands = commands;
  }

  createCellFooter(): ICellFooter {
    // Now that commands are a member of this class, you can pass them to CellFooterWithButton
    return new CellFooterWithButton(this.commands);
  }
}

// interface RunButtonProps {
//   commands: CommandRegistry;
// }

// class RunButton extends React.Component<RunButtonProps> {
//   private RUN_ICON = 'fa-solid fa-circle-play';
//   constructor(props: RunButtonProps, commands: CommandRegistry) {
//     super(props);    
//     this.handleRunClick = this.handleRunClick.bind(this);
//   }

//   handleRunClick() {
//     console.log("Clicked run cell");
//     this.props.commands.execute(COMMANDS.RUN_SELECTED_CODECELL);
//   }

//   render() {
//     return React.createElement(
//       'button',
//       {
//         className: CSS_CLASSES.CELL_FOOTER_BUTTON,
//         title: 'Click to run this cell',
//         onClick: () => this.handleRunClick(),
//       },
//       React.createElement('i', { className: this.RUN_ICON })
//     );
//   }
// }

/*
 * Extend the default implementation of a cell footer with custom buttons.
 */
class CellFooterWithButton extends ReactWidget implements ICellFooter {
  private readonly commands: CommandRegistry;
  private codeVisible: boolean = false;  
  private explVisible: boolean = false;
  private RUN_ICON = 'fa-solid fa-circle-play';
  private CLEAR_ICON = 'fa-solid fa-circle-xmark';
  private HIDE_ICON = 'fa-solid fa-eye-slash';
  private SHOW_ICON = 'fa-solid fa-eye';
  private EXPL_ICON = 'fa-solid fa-book';

  constructor(commands: CommandRegistry) {
    super();
    this.addClass(CSS_CLASSES.CELL_FOOTER);
    this.commands = commands;    
    
    // Add an event listener to the blue bar element
    this.node.addEventListener('click', (event) => {
    // Prevent the default behavior (collapsing/expanding)
      event.preventDefault();
    });
  }

  render() {
    const toggleIcon = this.codeVisible ? this.HIDE_ICON : this.SHOW_ICON;
        
    return React.createElement("div", {className: CSS_CLASSES.CELL_FOOTER_DIV }, 
      React.createElement("button", {
        className: CSS_CLASSES.CELL_FOOTER_BUTTON,
        title: "Toggle Explanation", //tooltip text
        onClick: () => {
          console.log("clicked explain");
          this.explVisible = !this.explVisible;
          this.commands.execute(COMMANDS.TOGGLE_EXPL_CELL);          
        },
      }, React.createElement("i", {className: this.EXPL_ICON })),

      React.createElement("button", {
        className: `${CSS_CLASSES.CELL_FOOTER_BUTTON} ${CSS_CLASSES.CELL_TOGGLE_BUTTON}`,
        title: "Click to hide or show code", //tooltip text
        onClick: () => {
          console.log("Clicked toggle cell visibility");
          this.codeVisible = !this.codeVisible;
          if (this.codeVisible) {
            this.commands.execute(COMMANDS.SHOW_CELL_CODE);
          } else {
            this.commands.execute(COMMANDS.HIDE_CELL_CODE);
          }
          this.update();
        },
      }, React.createElement("i", { className: toggleIcon })),
      
      React.createElement("button",{
        className: CSS_CLASSES.CELL_FOOTER_BUTTON,
        title: "Click to run this cell", //tooltip text
        onClick: () => {
          console.log("Clicked run cell");
          this.commands.execute(COMMANDS.RUN_SELECTED_CODECELL);
        },
      }, React.createElement("i", { className: this.RUN_ICON })),
        
      React.createElement("button", {
        className: CSS_CLASSES.CELL_FOOTER_BUTTON,
        title: "Click to clear cell output", //tooltip text
        onClick: () => {
          console.log("Clicked clear output");
          this.commands.execute(COMMANDS.CLEAR_SELECTED_OUTPUT);
        },
      }, React.createElement("i", { className: this.CLEAR_ICON }))
    );
  }
}

// Define a custom output area
export class CustomOutputArea extends OutputArea {
  constructor(commands: CommandRegistry) {
    // Create a RenderMimeRegistry instance
    const rendermime = new RenderMimeRegistry();

    super({
      rendermime, // Use the RenderMimeRegistry instance
      contentFactory: OutputArea.defaultContentFactory,
      model: new OutputAreaModel({ trusted: true }),
    });
    this.addClass(CSS_CLASSES.CUSTOM_OUTPUT_AREA);
  }
}

/**
 * Define a JupyterLab extension to add footer buttons to code cells.
 */
const footerButtonExtension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-cell_toolbar',
  autoStart: true,
  activate: activateCommands,
  requires: [INotebookTracker]
};


/**
 * Define a JupyterLab extension to override the default notebook cell factory.
 */
const cellFactory: JupyterFrontEndPlugin<NotebookPanel.IContentFactory> = {
  id: 'jupyter_bridge:plugin',
  description: 'A JupyterLab extension that adds footer buttons to code cells for improved interactivity and visibility control, supporting operations like running cells, hiding/showing code, and managing output directly from the cell interface. Initial functionality included to mark documentation cells that are controlled by their corresponding code cells.',
  provides: NotebookPanel.IContentFactory,
  requires: [IEditorServices],
  autoStart: true,
  activate: (app: JupyterFrontEnd, editorServices: IEditorServices) => {
    // tslint:disable-next-line:no-console
    console.log(
      'JupyterLab extension jupyter_bridge is activated!',
      'overrides default nootbook content factory'
    );

    const { commands } = app;
    const editorFactory = editorServices.factoryService.newInlineEditor;
    return new ContentFactoryWithFooterButton(commands, { editorFactory });
  }
};

/**
 * Export this plugins as default.
 */
const plugins: Array<JupyterFrontEndPlugin<any>> = [
  footerButtonExtension,
  cellFactory
];

export default plugins;
