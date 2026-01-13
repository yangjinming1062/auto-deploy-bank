# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SUSI.AI Skill CMS - A React-based web application for creating, editing, and managing SUSI.AI skills. Built with Create React App, Redux/DVA for state management, and Material-UI for components. The application serves as a content management system for SUSI.AI's conversational AI skills.

## Common Commands

### Development
- `npm start` - Start development server (runs on http://localhost:3000)
- `npm run build` - Build production bundle to `build/` directory
- `npm test` - Run full test suite with linting
- `npm test -- --watch` or `npm test -- --watchAll` - Run tests in watch mode

### Code Quality
- `npm run lint` - Run ESLint on all JavaScript files
- `npm run format` - Format code with Prettier
- Code formatting and linting are automatically run via `lint-staged` on git commit

### Deployment
- `npm run deploy` - Deploy to surge (after building)
- `npm run predeploy` - Automatically runs before deploy

## Architecture

### Core Technologies
- **React 16.8.6** with React Router v4
- **Redux/DVA** for state management (src/redux/)
- **Material-UI** (mixed v0.20.1 and @material-ui/core v3.9.3)
- **Node.js 8** (specified in .travis.yml)

### Entry Point
- `src/index.js:1` - Application entry point with routing configuration

### State Management Structure
```
src/redux/
├── actions/       # Redux action creators
├── reducers/      # Redux reducers
├── actionTypes.js # Action type constants
└── create.js      # DVA store creation
```

### Component Structure
```
src/components/
├── Admin/              # Admin panel components
├── Auth/               # Authentication (Login, SignUp, ForgotPassword)
├── AuthorSkills/       # Author's skill listings
├── BrowseSkill/        # Skill browsing and filtering
├── CreateSkill/        # Skill creation/editing
├── SkillEditor/        # Skill modification interface
├── SkillHistory/       # Version history viewing
├── SkillPage/          # Individual skill display
├── SkillVersion/       # Version information
├── StaticAppBar/       # Navigation bar
└── Dashboard/          # User dashboard
```

### API Integration
All SUSI.AI CMS API calls go through `src/api/` directory. Main API endpoint: `https://api.susi.ai/cms/`

Key endpoints (docs/ServerEndPoints.md:1):
- `getSkillList.json` - Fetch skill listings with filtering
- `getSkillsByAuthor.json` - Get skills by author
- `getGroups.json` - Get all skill groups
- `getAllLanguages.json` - Get all supported languages
- `createSkill.json` - Create new skill

### Routing Patterns
Main routes defined in `src/index.js:148`:
- `/` - BrowseSkill (home page)
- `/admin` - Admin panel
- `/dashboard` - User dashboard
- `/:category/:skill/:lang` - View skill
- `/:category/:skill/edit/:lang` - Edit skill
- `/:category/:skill/versions/:lang` - View versions
- `/:category/:skill/compare/:lang/:oldid/:recentid` - Compare versions
- `/category/:category` - Browse by category
- `/language/:language` - Browse by language

### Utilities
- `src/utils/` - Utility functions and helpers
- `src/DefaultSettings.js` - Application defaults
- `src/MUItheme.js` - Material-UI theme configuration

## Development Notes

### Testing
- Tests use **Jest** with **Enzyme** (React 16 adapter)
- Test files: `src/__tests__/`
- Setup: `src/setupTests.js:1`

### Code Style
- Linting: ESLint with Prettier integration
- Config: `.eslintrc` and `.prettierrc`
- Husky/lint-staged configured for pre-commit hooks

### Build System
- Built on Create React App (`react-scripts`)
- Output directory: `build/`
- Travis CI runs tests and deploys on successful builds

## Important Files

- `package.json:81` - Available npm scripts
- `.travis.yml:1` - CI/CD configuration
- `docs/ServerEndPoints.md:1` - API documentation
- `docs/FolderStructure.md:1` - Detailed folder structure guide
- `src/store.js:1` - Redux store configuration
- `public/index.html` - HTML template

## Key Dependencies

- React 16.8.6 with react-router-dom 4.3.1
- Material-UI v0.20.1 (legacy) and @material-ui/core 3.9.3 (newer)
- Redux 4.0.1 with redux-actions 2.6.4
- Axios 0.18.0 for API calls
- DVA 1.2.1 for data flow management

Note: This is a legacy codebase running React 16.8.6 and Node.js 8. Some dependencies are outdated.