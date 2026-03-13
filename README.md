# OneFS ChangeList Viewer

A blazing-fast, serverless, and fully responsive pure HTML/CSS/JS application to visually browse Dell PowerScale OneFS Changelist API results.

![OneFS ChangeList Viewer UI Preview](https://github.com/mupplelabs/OneFS_ChangeList_Viewer/blob/91905fe33fbb195939ff44094536926b9043e32a/screenshot.png)

## Overview
This tool is designed for administrators and developers working with the OneFS RESTful API. It takes JSON output from the `/10/changelist/<CHANGELIST>/entries` endpoint and provides a rich, interactive Explorer interface to navigate directory structures, uncover file moves, and filter changes by type and path.

## Features
- **Serverless Architecture**: Runs entirely in the browser. Zero dependencies, no backend, no installation required. Just open `index.html`.
- **Smart Move Detection**: Identifies file and directory movements/renames accurately using LIN matching, ID matching, and loose heuristic time-window correlation.
- **Directory Explorer Pane**: A collapsible, searchable tree-view mirroring the changed files' structure.
- **Advanced Filtering**: Filter rows by file type (e.g., `regular`, `dir`), specific change strings (e.g., `ENTRY_ADDED`, `WORM_COMMITTED`), or flexible text search.
- **Pure CSS Responsiveness**: The UI gracefully degrades from a 3-pane desktop layout down to an intuitive, auto-hiding CSS overlay system for tablets and smartphones. (Look ma, no JS toggles!).
- **Customizable Grid**: Select which columns you want to view, such as `Size`, `Physical Size`, `UID/GID`, `Parent LIN`, and timestamps.
- **Data Export**: Export your customized table view directly to `.csv` or `.json` for external reporting.
- **Syntax Highlighting**: Built-in JSON prettifying panel makes inspecting the raw API metadata simple and readable.
- **Theming**: Ships with VSCode-inspired Light and Dark modes. Share links with the preferred theme using URL parameters (e.g., `?theme=light`).

## Usage
1. Clone the repository or download the `index.html`, `styles.css`, and `app.js` files.
2. Open `index.html` in your favorite modern browser (Chrome, Edge, Firefox, Safari).
3. Use the **Open File** button to select your `.json` OneFS changelist dump.
4. Alternatively, click **Load Demo** to explore with mock data.

## Fetching Data from OneFS API
To generate the necessary JSON file for this tool, query the OneFS Platform API:
```bash
curl -u <username>:<password> -k \
  "https://<cluster-ip>:8080/platform/10/snapshot/changelists/<CHANGELIST>/entries" \
  > changelist_entries.json
```
*Note: Ensure your REST API user has the appropriate RBAC privileges to query changelists.*

## Customization
This tool was built to be easily customizable. If you need to add new columns from the API payload:
- **`app.js`**: Add new column objects to the `ALL_COLUMNS` array.
- **`styles.css`**: Tweak variables at the top of the file to match your organization's branding.

## License
MIT License. Feel free to use, modify, and distribute.
